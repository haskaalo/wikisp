package shortestpath;
import shortestpath.database.DatabaseHelper;
import java.sql.SQLException;

public class Main {
    public static void main(String[] args) {
        if (args.length != 2) {
            System.out.println("Invalid parameter length");
            return;
        }

        DatabaseHelper db;
        try {
            db = DatabaseHelper.connect();

            int id1 = db.getArticleIDByTitle(args[0]);
            if (id1 == -1) {
                System.out.println(String.format("\"%s\" is not a valid article name", args[0]));
                return;
            }
            int id2 = db.getArticleIDByTitle(args[1]);
            if (id2 == -1) {
                System.out.println(String.format("\"%s\" is not a valid article name", args[1]));
                return;
            }

            SimpleBFS bfs = new SimpleBFS();
            long start = System.nanoTime();
            System.out.println(bfs.compute(id1, id2));
            long end = System.nanoTime();

            System.out.println(String.format("Done in: %.2f", (end - start) / Math.pow(10, 9)));
        } catch (SQLException e) {
            System.out.println("Error while using database");
            System.out.println(e.getMessage());
        }
    }
}