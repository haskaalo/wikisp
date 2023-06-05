package shortestpath;

import com.esotericsoftware.kryo.Kryo;
import shortestpath.database.ArticleInfo;
import shortestpath.database.DatabaseHelper;
import java.io.FileOutputStream;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.HashMap;

import com.esotericsoftware.kryo.io.Output;

public class Main {
    public static void main(String[] args) {
        if (args.length > 0 && args[0].equals("serialize-list")) {
            Kryo kryo = new Kryo();
            kryo.register(ArticleAdjacencyList.class);
            kryo.register(HashMap.class);
            kryo.register(ArrayList.class);

            ArticleAdjacencyList adjacencyList = new ArticleAdjacencyList();
            adjacencyList.prepare();
            try {
                String destination = System.getenv("ADJACENCY_LIST_PATH");
                System.out.println("SERIALIZATION: Starting writing to disk at: " + destination);

                FileOutputStream fo = new FileOutputStream(destination);
                Output out = new Output(fo);

                kryo.writeObject(out, adjacencyList);

                out.close();
                fo.close();
                System.out.println("SERIALIZATION: Done! ");
            } catch (Exception e) {
                e.printStackTrace();
            }
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
            System.out.println("DONE LOADING SERIALIZED DATA");
            ArticleComponentExplorer expl = new ArticleComponentExplorer();
            if (info1.componentID != info2.componentID && !expl.existPossiblePath(info1.componentID, info2.componentID)) {
                System.out.println("NO PATH POSSIBLE!");
                return;
            }

            long start = System.nanoTime();
            System.out.println("\n" + bfs.compute(info1.id, info2.id));
            long end = System.nanoTime();

            System.out.println(String.format("Done in: %.2f", (end - start) / Math.pow(10, 9)));
        } catch (SQLException e) {
            System.out.println("Error while using database");
            System.out.println(e.getMessage());
        }
    }
}