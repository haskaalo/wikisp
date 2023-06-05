package shortestpath;

import shortestpath.database.DatabaseHelper;

import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicBoolean;


public class BidirectionalBFS {
    private DatabaseHelper db = DatabaseHelper.connect();

    public String compute(int source, int dest) {
        ConcurrentHashMap<Integer, PredecessorItem> predecessor = new ConcurrentHashMap<>();
        AtomicBoolean stopBrake = new AtomicBoolean();
        BFSThread sourceToDest = new BFSThread(source, dest, predecessor, true, stopBrake, 0);
        BFSThread destToSource = new BFSThread(dest, source, predecessor, false, stopBrake, 1);

        Thread t1 = new Thread(sourceToDest);
        Thread t2 = new Thread(destToSource);

        t1.start();
        t2.start();
        try {
            t1.join();
            t2.join();

            if (sourceToDest.getReturnValue() != null) {
                return String.join(" -> ", sourceToDest.getReturnValue());
            } else if (destToSource.getReturnValue() != null) {
                return String.join(" -> ", destToSource.getReturnValue());
            }
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }

        return "NO PATH FOUND!";
    }
}
