package shortestpath.lambdahandlers;

import com.amazonaws.auth.EnvironmentVariableCredentialsProvider;
import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;
import com.amazonaws.services.s3.model.GetObjectRequest;
import shortestpath.ComponentAdjacencyList;
import shortestpath.SimpleBFS;
import shortestpath.database.ArticleID;

import java.io.File;
import java.sql.SQLException;
import java.util.ArrayList;

public class ShortestPathHandler implements RequestHandler<ShortestPathEvent, ArrayList<Integer>[]> {
    private SimpleBFS bfs;
    private ComponentAdjacencyList expl;

    public ShortestPathHandler() {
        AmazonS3 s3Client = AmazonS3ClientBuilder.standard()
                .withCredentials(new EnvironmentVariableCredentialsProvider()).build();

        File articleMapFile = new File("/tmp/wdg_article_map.data");
        File componentMapFile = new File("/tmp/wdg_component_map.data");
        String bucket = System.getenv("AWS_S3_BUCKET");

        s3Client.getObject(new GetObjectRequest(bucket, "wdg_article_map.data"), articleMapFile);
        s3Client.getObject(new GetObjectRequest(bucket, "wdg_component_map.data"), componentMapFile);

        this.bfs = new SimpleBFS();
        this.expl = ComponentAdjacencyList.deserialize();
    }

    @Override
    public ArrayList<Integer>[] handleRequest(ShortestPathEvent event, Context context) {
        try {

            if (!expl.existPossiblePath(event.source.get(1), event.destination.get(1))) {
                return null;
            }

            ArrayList<ArticleID> result = bfs.compute(event.source.get(0), event.destination.get(0));
            if (result == null) return null;

            ArrayList<Integer> originalPathList = new ArrayList<>();
            ArrayList<Integer> finalPathList = new ArrayList<>();

            for (ArticleID ids : result) {
                originalPathList.add(ids.originalID);
                finalPathList.add(ids.finalID);
            }

            return (ArrayList<Integer>[]) new ArrayList[] { originalPathList, finalPathList };

        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }

}
