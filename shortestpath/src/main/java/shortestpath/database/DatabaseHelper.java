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

    public void close() {
        try {
            this.conn.close();
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }

    public ArrayList<Integer> getAdjacentArticles(int article_id, boolean outbound) throws SQLException {
        String query = """
                SELECT COALESCE(r.to_article, aled.to_article) as adjacent_id FROM article_link_edge_directed aled
                LEFT JOIN redirect r ON aled.to_article=r.from_article
                WHERE aled.from_article=?
                """;
        if (!outbound) {
            query = """
                SELECT COALESCE(r.to_article, aled.from_article) as adjacent_id FROM article_link_edge_directed aled
                LEFT JOIN redirect r ON aled.from_article=r.from_article
                WHERE aled.to_article=?
                """;
        }

        PreparedStatement stmt = this.conn.prepareStatement(query);
        stmt.setInt(1, article_id);

        ResultSet rs = stmt.executeQuery();

        ArrayList<Integer> listResult = new ArrayList<>();

        while (rs.next()) {
            listResult.add(rs.getInt("adjacent_id"));
        }

        return listResult;
    }

    public ArticleInfo getArticleInfoByTitle(String title) throws SQLException {
        String query = """
                SELECT COALESCE(r.to_article, a.id) as id, COALESCE(ca.component_id, a.component_id) as component_id FROM article a
                LEFT JOIN redirect r ON r.from_article=a.id
                LEFT JOIN article ca ON ca.id=r.to_article
                WHERE a.title=?
                """;

        PreparedStatement stmt = this.conn.prepareStatement(query);
        stmt.setString(1, title);

        ResultSet rs = stmt.executeQuery();
        if (!rs.next()) return null;

        return new ArticleInfo(rs.getInt("id"), rs.getInt("component_id"));
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

    public ArrayList<Integer> getAdjacentComponents(int componentID) {
        String query = "SELECT DISTINCT connects_to_id FROM article_component_connects WHERE component_id=?";

        try {
            PreparedStatement stmt = this.conn.prepareStatement(query);
            stmt.setInt(1, componentID);

            ArrayList<Integer> listResult = new ArrayList<>();
            ResultSet rs = stmt.executeQuery();
            while (rs.next()) {
                listResult.add(rs.getInt("connects_to_id"));
            }

            return listResult;
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }

    public ArrayList<Integer> getArticleIDList() {
        String query = "SELECT id FROM article where visited=1";

        try {
            Statement stmt = this.conn.createStatement();
            ResultSet rs = stmt.executeQuery(query);
            ArrayList<Integer> listResult = new ArrayList<>();

            while (rs.next()) {
                listResult.add(rs.getInt("id"));
            }

            return listResult;
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }
}
