package shortestpath;

import shortestpath.database.DatabaseHelper;

import java.sql.SQLException;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.Queue;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicBoolean;

public class BFSThread implements Runnable {
    private DatabaseHelper db = DatabaseHelper.connect();

    private int source, dest, threadID;

    private volatile ArrayList<String> returnVal = null;

    private ConcurrentHashMap<Integer, PredecessorItem> predecessor;
    private boolean outbound;

    private AtomicBoolean stopBrake;

    public BFSThread(int source, int dest,
                     ConcurrentHashMap<Integer, PredecessorItem> predecessor, boolean outbound,
                     AtomicBoolean stopBrake,
                     int threadID) {
        this.source = source;
        this.dest = dest;
        this.predecessor = predecessor;
        this.outbound = outbound;
        this.threadID = threadID;
        this.stopBrake = stopBrake;
    }

    private ArrayList<String> predecessorPath(int dest) {
        int current = dest;
        ArrayList<String> path = new ArrayList<>();

        while (current != -1) {
            if (this.outbound) {
                path.add(0, db.getArticleTitleByID(current));
            } else {
                path.add(db.getArticleTitleByID(current));
            }
            current = predecessor.get(current).val;
        }

        return path;
    }

    public ArrayList<String> getReturnValue() {
        return this.returnVal;
    }

    @Override
    public void run() {
        Queue<Integer> bfsQueue = new LinkedList<>();

        bfsQueue.add(this.source);
        predecessor.put(this.source, new PredecessorItem(-1, this.threadID));

        while (!bfsQueue.isEmpty()) {
            if (stopBrake.get()) break;

            int articleID = bfsQueue.poll();

            // TODO TESTS
            System.out.print("\r"+predecessor.size());

            try {
                ArrayList<Integer> adjacentArticlesID = this.db.getAdjacentArticles(articleID, this.outbound);

                for (int adjacentArticleID : adjacentArticlesID) {
                    PredecessorItem p;
                    if ((p = predecessor.get(adjacentArticleID)) != null) {
                        if (p.threadID != this.threadID) {
                            ArrayList<String> otherThreadPath = this.predecessorPath(adjacentArticleID);
                            ArrayList<String> thisThreadPath = this.predecessorPath(articleID);

                            if (this.outbound) {
                                thisThreadPath.addAll(otherThreadPath);
                                this.returnVal = thisThreadPath;
                            } else {
                                otherThreadPath.addAll(thisThreadPath);
                                this.returnVal = otherThreadPath;
                            }
                            this.stopBrake.set(true);

                            break;
                        }

                        continue;
                    }

                    this.predecessor.put(adjacentArticleID, new PredecessorItem(articleID, this.threadID));

                    if (adjacentArticleID == dest) {
                        this.returnVal = this.predecessorPath(dest);
                        this.stopBrake.set(true);
                        break;
                    }

                    bfsQueue.add(adjacentArticleID);
                }
            } catch (SQLException e) {
                throw new RuntimeException(e);
            }

        }

        this.db.close();
    }
}
