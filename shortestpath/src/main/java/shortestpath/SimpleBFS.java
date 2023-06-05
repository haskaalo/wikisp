package shortestpath;

import shortestpath.database.DatabaseHelper;

import java.sql.SQLException;
import java.util.*;

public class SimpleBFS {
    private DatabaseHelper db = DatabaseHelper.connect();
    private HashMap<Integer, ArrayList<Integer>> adjacencyMap = new HashMap<>();

    private String predecessorPath(HashMap<Integer, Integer> predecessor, int dest) {
        if (dest == -1) return "";

        String arrow = " -> ";

        if (predecessor.get(dest) == -1) arrow = "";

        return predecessorPath(predecessor, predecessor.get(dest)) + arrow + db.getArticleTitleByID(dest);
    }

    public String compute(int article1_id, int article2_id) throws SQLException {
        Queue<Integer> bfsQueue = new LinkedList<>();
        HashMap<Integer, Integer> predecessor = new HashMap<>();

        bfsQueue.add(article1_id);
        predecessor.put(article1_id, -1);

        while (!bfsQueue.isEmpty()) {
            int articleID = bfsQueue.poll();

            ArrayList<Integer> adjacentArticlesID = this.db.getAdjacentArticles(articleID, true);

            System.out.print("\r"+predecessor.size() + " " + bfsQueue.size());

            for (int adjacentArticleID : adjacentArticlesID) {
                if (predecessor.containsKey(adjacentArticleID)) continue;

                predecessor.put(adjacentArticleID, articleID);

                if (adjacentArticleID == article2_id) {
                    return predecessorPath(predecessor, article2_id);
                }

                bfsQueue.add(adjacentArticleID);
            }
        }

        return "NO PATH FOUND!";
    }
}
