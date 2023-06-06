package shortestpath;

import com.esotericsoftware.kryo.Kryo;
import com.esotericsoftware.kryo.io.Input;
import com.esotericsoftware.kryo.io.Output;
import shortestpath.database.ArticleID;
import shortestpath.database.DatabaseHelper;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.nio.file.Paths;
import java.util.*;

public class ComponentAdjacencyList {
    private HashMap<Integer, ArrayList<Integer>> componentAdjacencyMap = new HashMap<>();

    public ComponentAdjacencyList() {

    }

    public ComponentAdjacencyList(HashMap<Integer, ArrayList<Integer>> componentAdjacencyMap) {
        this.componentAdjacencyMap = componentAdjacencyMap;
    }

    public void prepare() {
        DatabaseHelper db = DatabaseHelper.connect();

        System.out.println("SERIALIZATION: Fetching component ID list");
        ArrayList<Integer> componentList = db.getArticleComponentIDList();
        System.out.println("SERIALIZATION: Done fetching component ID list ");
        System.out.println("SERIALIZATION: Starting building adjacency list\n");

        for (int componentID : componentList) {
            if (componentAdjacencyMap.containsKey(componentID)) continue;

            this.performBFS(componentID, db);
        }

        String destination = Paths.get(System.getenv("ADJACENCY_LIST_PATH"), "wdg_component_map.data")
                .toString();

        System.out.println("SERIALIZATION: Starting writing to disk at: " + destination);

        Kryo kryo = new Kryo();
        kryo.register(ArrayList.class);
        kryo.register(HashMap.class);

        try {
            FileOutputStream fo = new FileOutputStream(destination);
            Output out = new Output(fo);
            kryo.writeObject(out, componentAdjacencyMap);

            out.close();
            fo.close();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }

        db.close();
    }

    public static ComponentAdjacencyList deserialize() {
        try {
            Kryo kryo = new Kryo();
            kryo.register(ArrayList.class);
            kryo.register(HashMap.class);

            String adjacencyMapPath = Paths.get(System.getenv("ADJACENCY_LIST_PATH"), "wdg_component_map.data")
                    .toString();
            Input input = new Input(new FileInputStream(adjacencyMapPath));
            HashMap<Integer, ArrayList<Integer>> listResult = kryo.readObject(input, HashMap.class);
            input.close();

            return new ComponentAdjacencyList(listResult);
        } catch (FileNotFoundException e) {
            throw new RuntimeException(e);
        }
    }

    private void performBFS(int startingComponent, DatabaseHelper db) {
        Queue<Integer> bfsQueue = new LinkedList<>();
        HashSet<Integer> visitedArticles = new HashSet<>();

        bfsQueue.add(startingComponent);

        while (!bfsQueue.isEmpty()) {
            int articleID = bfsQueue.poll();

            ArrayList<Integer> adjacentArticlesID = db.getAdjacentComponents(articleID);

            componentAdjacencyMap.put(articleID, adjacentArticlesID);

            for (int adjacentArticleID : adjacentArticlesID) {
                if (visitedArticles.contains(adjacentArticleID)) continue;
                else if (this.componentAdjacencyMap.containsKey(adjacentArticleID)) continue;

                visitedArticles.add(adjacentArticleID);
                bfsQueue.add(adjacentArticleID);
            }
        }
    }

    public boolean existPossiblePath(int fromComponentID, int toComponentID) {
        Queue<Integer> bfsQueue = new LinkedList<>();
        HashSet<Integer> visitedComponents = new HashSet<>();

        bfsQueue.add(fromComponentID);
        visitedComponents.add(fromComponentID);

        while (!bfsQueue.isEmpty()) {
            int componentID = bfsQueue.poll();

            ArrayList<Integer> adjacentComponents = this.componentAdjacencyMap.get(componentID);

            for (int adjacentComponentID : adjacentComponents) {
                if (visitedComponents.contains(adjacentComponentID)) continue;

                visitedComponents.add(adjacentComponentID);

                if (adjacentComponentID == toComponentID) return true;

                bfsQueue.add(adjacentComponentID);
            }
        }

        return false;
    }
}
