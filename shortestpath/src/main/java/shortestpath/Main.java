package shortestpath;

import shortestpath.database.ArticleID;
import shortestpath.database.ArticleInfo;
import shortestpath.database.DatabaseHelper;

import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        if (args.length > 0 && args[0].equals("serialize")) {
            ArticleAdjacencyList articleAdjacencyList = new ArticleAdjacencyList();
            ComponentAdjacencyList componentAdjacencyList = new ComponentAdjacencyList();

            articleAdjacencyList.prepare();
            componentAdjacencyList.prepare();
            return;
        }

        if (args.length != 2) {
            System.out.println("Invalid parameter length");
            return;
        }

        DatabaseHelper db;
        try {
            db = DatabaseHelper.connect();

            ArticleInfo info1 = db.getArticleInfoByTitle(args[0]);
            if (info1 == null) {
                System.out.println(String.format("\"%s\" is not a valid article name", args[0]));
                return;
            }
            ArticleInfo info2 = db.getArticleInfoByTitle(args[1]);
            if (info2 == null) {
                System.out.println(String.format("\"%s\" is not a valid article name", args[1]));
                return;
            }

            System.out.println("LOADING SERIALIZED DATA");
            SimpleBFS bfs = new SimpleBFS();
            ComponentAdjacencyList expl = ComponentAdjacencyList.deserialize();
            System.out.println("DONE LOADING SERIALIZED DATA");

            if (info1.componentID != info2.componentID && !expl.existPossiblePath(info1.componentID, info2.componentID)) {
                System.out.println("NO PATH POSSIBLE!");
                return;
            }

            long start = System.nanoTime();
            ArrayList<ArticleID> result = bfs.compute(info1.id, info2.id);
            long end = System.nanoTime();

            if (result == null) {
                System.out.println("NO PATH POSSIBLE!!!");
                return;
            }

            List<String> resultFinalString = result
                    .stream().map(dest -> db.getArticleTitleByID(dest.finalID)).toList();

            List<String> resultOriginalString = result
                    .stream().map(dest -> db.getArticleTitleByID(dest.originalID)).toList();

            System.out.println("\n" + String.join(" -> ", resultFinalString));
            System.out.println(String.join(" -> ", resultOriginalString));

            System.out.println(String.format("Done in: %.2f", (end - start) / Math.pow(10, 9)));
        } catch (SQLException e) {
            System.out.println("Error while using database");
            System.out.println(e.getMessage());
        }
    }
}