package shortestpath;

import shortestpath.database.DatabaseHelper;

import java.util.*;

public class ArticleComponentExplorer {
    private DatabaseHelper db = DatabaseHelper.connect();

    public boolean existPossiblePath(int fromComponentID, int toComponentID) {
        Queue<Integer> bfsQueue = new LinkedList<>();
        HashSet<Integer> visitedComponents = new HashSet<>();

        bfsQueue.add(fromComponentID);
        visitedComponents.add(fromComponentID);

        while (!bfsQueue.isEmpty()) {
            int componentID = bfsQueue.poll();

            ArrayList<Integer> adjacentComponents = this.db.getAdjacentComponents(componentID);

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
