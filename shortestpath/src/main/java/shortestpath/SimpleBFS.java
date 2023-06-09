package shortestpath;

import shortestpath.database.ArticleID;
import java.sql.SQLException;
import java.util.*;

public class SimpleBFS {
    private ArticleAdjacencyList adjacencyMap = ArticleAdjacencyList.deserialize();

    private ArrayList<ArticleID> predecessorPath(HashMap<Integer, ArticleID> predecessor, ArticleID dest) {
        ArrayList<ArticleID> result = new ArrayList<>();
        while (dest != null) {
            result.add(dest);
            dest = predecessor.get(dest.finalID);
        }

        Collections.reverse(result);

        return result;
    }

    public ArrayList<ArticleID> compute(int article1_id, int article2_id) throws SQLException {
        Queue<ArticleID> bfsQueue = new LinkedList<>();
        HashMap<Integer, ArticleID> predecessor = new HashMap<>();

        bfsQueue.add(new ArticleID(article1_id, article1_id));
        predecessor.put(article1_id, null);

        while (!bfsQueue.isEmpty()) {
            ArticleID articleID = bfsQueue.poll();

            ArrayList<ArticleID> adjacentArticlesID = this.adjacencyMap.get(articleID.finalID);

            System.out.print("\r"+predecessor.size() + " " + bfsQueue.size());

            for (ArticleID adjacentArticleID : adjacentArticlesID) {
                if (predecessor.containsKey(adjacentArticleID.finalID)) continue;

                predecessor.put(adjacentArticleID.finalID, articleID);

                if (adjacentArticleID.finalID == article2_id) {
                    return predecessorPath(predecessor, adjacentArticleID);
                }

                bfsQueue.add(adjacentArticleID);
            }
        }

        return null;
    }
}
