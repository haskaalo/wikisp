package shortestpath.database;

import java.sql.*;
import java.util.ArrayList;

public class DatabaseHelper {
    private Connection conn;

    public DatabaseHelper(Connection connection) {
        this.conn = connection;
    }

    public static DatabaseHelper connect() {
        String connURL = "jdbc:sqlite:" + System.getenv("SQLITE3_DB_PATH");

        try {
            return new DatabaseHelper(DriverManager.getConnection(connURL));
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }

    public void close() throws SQLException {
        this.conn.close();
    }

    public ArrayList<Integer> getAdjacentArticles(int article_id) throws SQLException {
        String query = """
                SELECT COALESCE(r.to_article, aled.to_article) as adjacent_id FROM article_link_edge_directed aled
                LEFT JOIN redirect r ON aled.to_article=r.from_article
                WHERE aled.from_article=?
                """;

        PreparedStatement stmt = this.conn.prepareStatement(query);
        stmt.setInt(1, article_id);

        ResultSet rs = stmt.executeQuery();

        ArrayList<Integer> listResult = new ArrayList<>();

        while (rs.next()) {
            listResult.add(rs.getInt("adjacent_id"));
        }

        return listResult;
    }

    public int getArticleIDByTitle(String title) throws SQLException {
        String query = """
                SELECT COALESCE(r.to_article, id) as id FROM article
                LEFT JOIN redirect r ON r.from_article=id
                WHERE title=?
                """;

        PreparedStatement stmt = this.conn.prepareStatement(query);
        stmt.setString(1, title);

        ResultSet rs = stmt.executeQuery();
        if (!rs.next()) return -1;

        return rs.getInt("id");
    }

    public String getArticleTitleByID(int id) {
        String query = "SELECT title FROM article WHERE id=?";

        try {
            PreparedStatement stmt = this.conn.prepareStatement(query);
            stmt.setInt(1, id);

            ResultSet rs = stmt.executeQuery();
            if (!rs.next()) return null;

            return rs.getString("title");
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }
}
