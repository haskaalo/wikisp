package shortestpath;

import com.esotericsoftware.kryo.Kryo;
import com.esotericsoftware.kryo.io.Input;
import com.esotericsoftware.kryo.io.Output;
import shortestpath.database.ArticleID;
import shortestpath.database.DatabaseHelper;

import java.io.*;
import java.sql.SQLException;
import java.util.*;

public class ArticleAdjacencyList implements Serializable {

    // Theres around 200m+ connections, so around 2gb? (200m x (4 + 4)) bytes
    private HashMap<Integer, ArrayList<ArticleID>> adjacencyList = new HashMap<>();

    public ArticleAdjacencyList(HashMap<Integer, ArrayList<ArticleID>> adjacencyList) {
        this.adjacencyList = adjacencyList;
    }

    public ArticleAdjacencyList() {

    }

    public void prepare() {
        DatabaseHelper db = DatabaseHelper.connect();

        System.out.println("SERIALIZATION: Fetching article ID list");
        ArrayList<Integer> articleList = db.getArticleIDList();
        System.out.println("SERIALIZATION: Done fetching article ID list ");
        System.out.println("SERIALIZATION: Starting building adjacency list\n");

        for (int articleID : articleList) {
            if (adjacencyList.containsKey(articleID)) continue;

            try {
                this.performBFS(articleID, db);
            } catch (SQLException e) {
                throw new RuntimeException(e);
            }
        }

        String destination = System.getenv("ADJACENCY_LIST_PATH");
        System.out.println("SERIALIZATION: Starting writing to disk at: " + destination);

        Kryo kryo = new Kryo();
        kryo.register(ArticleID.class);
        kryo.register(ArrayList.class);
        kryo.register(HashMap.class);

        try {
            FileOutputStream fo = new FileOutputStream(destination);
            Output out = new Output(fo);
            kryo.writeObject(out, adjacencyList);

            out.close();
            fo.close();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }

        System.out.println("SERIALIZATION: Done! ");

        System.out.println("SERIALIZATION: Done building adjacency map");
        db.close();
    }

    private void performBFS(int startingNode, DatabaseHelper db) throws SQLException {
        Queue<Integer> bfsQueue = new LinkedList<>();
        HashSet<Integer> visitedArticles = new HashSet<>();

        bfsQueue.add(startingNode);

        while (!bfsQueue.isEmpty()) {
            int articleID = bfsQueue.poll();

            ArrayList<ArticleID> adjacentArticlesID = db.getAdjacentArticles(articleID, true);

            System.out.print("\r"+ adjacencyList.size() + " " + bfsQueue.size());

            adjacencyList.put(articleID, adjacentArticlesID);

            for (ArticleID adjacentArticleID : adjacentArticlesID) {
                if (visitedArticles.contains(adjacentArticleID.finalID)) continue;
                else if (this.adjacencyList.containsKey(adjacentArticleID.finalID)) continue;

                visitedArticles.add(adjacentArticleID.finalID);
                bfsQueue.add(adjacentArticleID.finalID);
            }
        }
    }

    public static ArticleAdjacencyList deserialize() {
        try {
            Kryo kryo = new Kryo();
            kryo.register(ArticleID.class);
            kryo.register(ArrayList.class);
            kryo.register(HashMap.class);
            kryo.register(ArticleAdjacencyList.class);

            String adjacencyMapPath = System.getenv("ADJACENCY_LIST_PATH");
            if (adjacencyMapPath != null) {
                Input input = new Input(new FileInputStream(adjacencyMapPath));
                HashMap<Integer, ArrayList<ArticleID>> listResult = kryo.readObject(input, HashMap.class);
                input.close();

                return new ArticleAdjacencyList(listResult);
            } else {
                throw new RuntimeException("Called loadArticleAdjacencyList while serialized file don't exist");
            }
        } catch (FileNotFoundException e) {
            throw new RuntimeException(e);
        }
    }

    public ArrayList<ArticleID> get(Integer key) {
        return this.adjacencyList.get(key);
    }

    public boolean containsKey(Integer key) {
        return this.adjacencyList.containsKey(key);
    }
}
