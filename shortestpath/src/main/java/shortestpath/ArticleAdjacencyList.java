package shortestpath;

import shortestpath.database.DatabaseHelper;

import java.io.Serializable;
import java.sql.SQLException;
import java.util.*;

public class ArticleAdjacencyList implements Serializable {

    // Theres around 200m+ connections, so around 2gb? (200m x (4 + 4)) bytes
    private HashMap<Integer, ArrayList<Integer>> adjacencyList = new HashMap<>();

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
        System.out.println("SERIALIZATION: Done building adjacency map");
        db.close();
    }

    private void performBFS(int startingNode, DatabaseHelper db) throws SQLException {
        Queue<Integer> bfsQueue = new LinkedList<>();
        HashSet<Integer> visitedArticles = new HashSet<>();

        bfsQueue.add(startingNode);

        while (!bfsQueue.isEmpty()) {
            int articleID = bfsQueue.poll();

            ArrayList<Integer> adjacentArticlesID = db.getAdjacentArticles(articleID, true);

            System.out.print("\r"+ adjacencyList.size() + " " + bfsQueue.size());

            adjacencyList.put(articleID, adjacentArticlesID);

            for (int adjacentArticleID : adjacentArticlesID) {
                if (visitedArticles.contains(adjacentArticleID)) continue;
                else if (this.adjacencyList.containsKey(adjacentArticleID)) continue;

                visitedArticles.add(adjacentArticleID);
                bfsQueue.add(adjacentArticleID);
            }
        }
    }

    public ArrayList<Integer> get(Integer key) {
        return this.adjacencyList.get(key);
    }

    public boolean containsKey(Integer key) {
        return this.adjacencyList.containsKey(key);
    }
}
