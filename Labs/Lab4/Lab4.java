import java.util.Date;
import java.util.concurrent.locks.ReentrantLock;

public class Philosophers {

    static int philosopherNum = 5;
    static Philosopher[] philosophers = new Philosopher[philosopherNum];
    static Fork[] Forks = new Fork[philosopherNum];

    static class Fork {
        public ReentrantLock mutex = new ReentrantLock();
        void grab() {
            try {
                mutex.tryLock();
            }
            catch (Exception e) {
                e.printStackTrace(System.out);
            }
        }

        void release() {
            mutex.unlock();
        }

        boolean isFree() {
            return !mutex.isLocked();
        }
    }


    static class Philosopher extends Thread {
        public int number;
        public Fork leftFork;
        public Fork rightFork;

        Philosopher(int num, Fork left, Fork right) {
            number = num;
            leftFork = left;
            rightFork = right;
        }

        public void run() {
            while (true) {
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                int state = (int)(Math.random() * 5);
                switch (state) {
                    case 0:
                        if (!(leftFork.mutex.isHeldByCurrentThread()) && leftFork.isFree()) {
                            leftFork.grab();
                            System.out.println(System.nanoTime() + ": " + "Философ №" + (number + 1) + " берёт левую вилку.");
                        }
                    case 1:
                        if (!(rightFork.mutex.isHeldByCurrentThread()) && rightFork.isFree()) {
                            rightFork.grab();
                            System.out.println(System.nanoTime() + ":  " + "Философ №" + (number + 1) + " берёт правую вилку.");
                        }
                    case 2:     // если есть обе вилки, то есть
                        if (leftFork.mutex.isHeldByCurrentThread() && rightFork.mutex.isHeldByCurrentThread()) {
                            int sleepTime = (int)(Math.random() * 3000);
                            System.out.println(System.nanoTime() + ":  " + "Философ №" + (number+1) + " собирается есть в течение " + sleepTime +"мс");
                            try {
                                Thread.sleep(sleepTime);
                            } catch (InterruptedException e) {
                                e.printStackTrace();
                            }
                        }
                        break;
                    case 3:
                        if (leftFork.mutex.isHeldByCurrentThread()) {
                            leftFork.release();
                            System.out.println(System.nanoTime() + ":  " + "Философ №" + (number + 1) + " кладёт левую вилку на место.");
                        }
                        if (rightFork.mutex.isHeldByCurrentThread()) {
                            rightFork.release();
                            System.out.println(System.nanoTime() + ":  " + "Философ №" + (number + 1) + " кладёт правую вилку на место.");
                        }
                        break;
                    case 4:
                        int sleepTime = (int)(Math.random() * 2000);
                        System.out.println(System.nanoTime() + ":  " + "Философ №" + (number+1) + " собирается размышлять в течение " + sleepTime +"мс");
                        try {
                            Thread.sleep(sleepTime);
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
                        break;
                }
            }
        }
    }


public static void main(String[] args) {

        for (int i = 0; i < philosopherNum; i++) {
            Forks[i] = new Fork();
        }
        for (int i = 0; i < philosopherNum; i++) {
            philosophers[i] = new Philosopher(i, Forks[i], Forks[(i + 1) % philosopherNum]);
            philosophers[i].start();
        }
        long startTime = System.currentTimeMillis();
        long elapsedTime = 0L;
        while (elapsedTime < 30 * 1000) {
            try {
                elapsedTime = (new Date()).getTime() - startTime;
                Thread.sleep(1000);
                boolean deadlock = true;
                for (Fork fs : Forks) {
                    if (fs.isFree()) {
                        deadlock = false;
                        break;
                    }
                }
                if (deadlock) {
                    for (Fork fs : Forks) {
                        if (fs.mutex.isHeldByCurrentThread()) fs.mutex.unlock();
                    }
                    System.out.println(System.nanoTime() + ":  " + "Все кладут вилки на стол");
                }
            }
            catch (Exception e) {
                e.printStackTrace(System.out);
            }
        }
        System.exit(0);
    }
}