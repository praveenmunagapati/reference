# java_chunk3.py
# Phase 4: All 23 Gang of Four Design Patterns in modern Java

chunk_content = r"""
        // ====================================================================
        // 4.1  Creational Patterns — Singleton, Factory Method, Abstract Factory, Builder, Prototype
        // ====================================================================

        // --- 1. Singleton ---
        static class DatabaseConnection {
            private DatabaseConnection() {
                System.out.println("  [Singleton] Created connection to production database.");
            }
            private static class Holder {
                private static final DatabaseConnection INSTANCE = new DatabaseConnection();
            }
            static DatabaseConnection getInstance() { return Holder.INSTANCE; }
            void executeQuery(String sql) { System.out.println("  [DB] Executing: " + sql); }
        }

        // --- 2. Factory Method ---
        interface Notification { void notifyUser(); }
        static class EmailNotification implements Notification {
            @Override public void notifyUser() { System.out.println("  [Email] Hello from email!"); }
        }
        static class SMSNotification implements Notification {
            @Override public void notifyUser() { System.out.println("  [SMS] Hello from SMS!"); }
        }
        static abstract class NotificationFactory {
            abstract Notification createNotification();
            void sendNotification() {
                Notification note = createNotification();
                note.notifyUser();
            }
        }
        static class EmailNotificationFactory extends NotificationFactory {
            @Override Notification createNotification() { return new EmailNotification(); }
        }
        static class SMSNotificationFactory extends NotificationFactory {
            @Override Notification createNotification() { return new SMSNotification(); }
        }

        // --- 3. Abstract Factory ---
        interface Button { void paint(); }
        interface Checkbox { void paint(); }
        static class WinButton implements Button {
            @Override public void paint() { System.out.println("  [WinButton] Painting windows button."); }
        }
        static class WinCheckbox implements Checkbox {
            @Override public void paint() { System.out.println("  [WinCheckbox] Painting windows checkbox."); }
        }
        static class MacButton implements Button {
            @Override public void paint() { System.out.println("  [MacButton] Painting mac button."); }
        }
        static class MacCheckbox implements Checkbox {
            @Override public void paint() { System.out.println("  [MacCheckbox] Painting mac checkbox."); }
        }
        interface GUIFactory {
            Button createButton();
            Checkbox createCheckbox();
        }
        static class WinFactory implements GUIFactory {
            @Override public Button createButton() { return new WinButton(); }
            @Override public Checkbox createCheckbox() { return new WinCheckbox(); }
        }
        static class MacFactory implements GUIFactory {
            @Override public Button createButton() { return new MacButton(); }
            @Override public Checkbox createCheckbox() { return new MacCheckbox(); }
        }

        // --- 4. Builder ---
        static class HttpRequest {
            private final String method, url, body;
            private final Map<String, String> headers;
            private final int timeout;

            private HttpRequest(Builder b) {
                this.method = b.method; this.url = b.url; this.body = b.body;
                this.headers = b.headers; this.timeout = b.timeout;
            }

            static class Builder {
                private String method = "GET", url, body = "";
                private final Map<String, String> headers = new HashMap<>();
                private int timeout = 5000;

                Builder url(String url) { this.url = url; return this; }
                Builder method(String m) { this.method = m; return this; }
                Builder header(String k, String v) { this.headers.put(k, v); return this; }
                Builder body(String body) { this.body = body; return this; }
                Builder timeout(int t) { this.timeout = t; return this; }
                HttpRequest build() { return new HttpRequest(this); }
            }

            @Override
            public String toString() {
                return String.format("HttpRequest(method=%s, url=%s, headers=%s, body='%s', timeout=%d)",
                                     method, url, headers, body, timeout);
            }
        }

        // --- 5. Prototype ---
        static abstract class ShapePrototype implements Cloneable {
            String type;
            abstract void draw();
            @Override
            public Object clone() {
                Object clone = null;
                try { clone = super.clone(); }
                catch (CloneNotSupportedException e) { e.printStackTrace(); }
                return clone;
            }
        }
        static class CirclePrototype extends ShapePrototype {
            CirclePrototype() { type = "Circle"; }
            @Override void draw() { System.out.println("  [Prototype] Drawing Circle"); }
        }

        // ====================================================================
        // 4.2  Structural Patterns — Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy
        // ====================================================================

        // --- 6. Adapter ---
        static class LegacyPrinter {
            void printOld(String msg) { System.out.println("  [Legacy] " + msg); }
        }
        interface ModernPrinter { void printNew(String msg); }
        static class PrinterAdapter implements ModernPrinter {
            private final LegacyPrinter legacyPrinter;
            PrinterAdapter(LegacyPrinter lp) { this.legacyPrinter = lp; }
            @Override
            public void printNew(String msg) { legacyPrinter.printOld(msg); }
        }

        // --- 7. Bridge ---
        interface DrawAPI { void drawCircle(int radius, int x, int y); }
        static class RedCircle implements DrawAPI {
            @Override public void drawCircle(int r, int x, int y) {
                System.out.printf("  [Bridge] Red Circle: radius=%d (%d,%d)%n", r, x, y);
            }
        }
        static class GreenCircle implements DrawAPI {
            @Override public void drawCircle(int r, int x, int y) {
                System.out.printf("  [Bridge] Green Circle: radius=%d (%d,%d)%n", r, x, y);
            }
        }
        static abstract class ShapeBridge {
            protected DrawAPI drawAPI;
            protected ShapeBridge(DrawAPI api) { this.drawAPI = api; }
            abstract void draw();
        }
        static class CircleBridge extends ShapeBridge {
            private final int x, y, radius;
            CircleBridge(int x, int y, int r, DrawAPI api) {
                super(api); this.x = x; this.y = y; this.radius = r;
            }
            @Override void draw() { drawAPI.drawCircle(radius, x, y); }
        }

        // --- 8. Composite ---
        interface Graphic { void print(); }
        static class LeafGraphic implements Graphic {
            private final String name;
            LeafGraphic(String n) { this.name = n; }
            @Override public void print() { System.out.println("    Leaf: " + name); }
        }
        static class CompositeGraphic implements Graphic {
            private final List<Graphic> children = new ArrayList<>();
            void add(Graphic g) { children.add(g); }
            @Override
            public void print() {
                System.out.println("  Composite:");
                for (Graphic g : children) g.print();
            }
        }

        // --- 9. Decorator ---
        interface DataSource {
            void writeData(String data);
            String readData();
        }
        static class FileDataSource implements DataSource {
            private String content;
            @Override public void writeData(String d) { this.content = d; }
            @Override public String readData() { return content; }
        }
        static abstract class DataSourceDecorator implements DataSource {
            protected DataSource wrappee;
            DataSourceDecorator(DataSource ds) { this.wrappee = ds; }
            @Override public void writeData(String d) { wrappee.writeData(d); }
            @Override public String readData() { return wrappee.readData(); }
        }
        static class EncryptionDecorator extends DataSourceDecorator {
            EncryptionDecorator(DataSource ds) { super(ds); }
            @Override
            public void writeData(String d) {
                super.writeData(rot13(d));
            }
            @Override
            public String readData() {
                return rot13(super.readData());
            }
            private String rot13(String s) {
                if (s == null) return null;
                StringBuilder sb = new StringBuilder();
                for (char c : s.toCharArray()) {
                    if (c >= 'a' && c <= 'm') c += 13;
                    else if (c >= 'n' && c <= 'z') c -= 13;
                    else if (c >= 'A' && c <= 'M') c += 13;
                    else if (c >= 'N' && c <= 'Z') c -= 13;
                    sb.append(c);
                }
                return sb.toString();
            }
        }

        // --- 10. Facade ---
        static class CPU {
            void freeze() { System.out.println("    [CPU] Freeze."); }
            void jump(long position) { System.out.println("    [CPU] Jump to " + position); }
            void execute() { System.out.println("    [CPU] Execute instructions."); }
        }
        static class HardDrive {
            void read(long lba, int size) { System.out.println("    [HDD] Read " + size + " bytes from sector " + lba); }
        }
        static class Memory {
            void load(long position, byte[] data) { System.out.println("    [Memory] Load bytes to " + position); }
        }
        static class ComputerFacade {
            private final CPU cpu = new CPU();
            private final Memory memory = new Memory();
            private final HardDrive hdd = new HardDrive();
            void start() {
                cpu.freeze();
                hdd.read(0, 1024);
                memory.load(0x00, new byte[]{0x00});
                cpu.jump(0x00);
                cpu.execute();
            }
        }

        // --- 11. Flyweight ---
        interface Flyweight { void operation(int extrinsicState); }
        static class ConcreteFlyweight implements Flyweight {
            private final String intrinsicState;
            ConcreteFlyweight(String intrinsic) { this.intrinsicState = intrinsic; }
            @Override
            public void operation(int extrinsic) {
                System.out.printf("    [Flyweight] Intrinsic: %s, Extrinsic: %d%n", intrinsicState, extrinsic);
            }
        }
        static class FlyweightFactory {
            private final Map<String, Flyweight> cache = new HashMap<>();
            Flyweight getFlyweight(String key) {
                return cache.computeIfAbsent(key, ConcreteFlyweight::new);
            }
        }

        // --- 12. Proxy ---
        interface Image { void display(); }
        static class RealImage implements Image {
            private final String filename;
            RealImage(String fn) {
                this.filename = fn;
                loadFromDisk();
            }
            private void loadFromDisk() { System.out.println("    [RealImage] Loading " + filename); }
            @Override public void display() { System.out.println("    [RealImage] Displaying " + filename); }
        }
        static class ProxyImage implements Image {
            private RealImage realImage;
            private final String filename;
            ProxyImage(String fn) { this.filename = fn; }
            @Override
            public void display() {
                if (realImage == null) realImage = new RealImage(filename);
                System.out.println("    [ProxyImage] Access logs verified.");
                realImage.display();
            }
        }

        // ====================================================================
        // 4.3  Behavioral Patterns — Chain of Responsibility, Command, Interpreter, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor
        // ====================================================================

        // --- 13. Chain of Responsibility ---
        static abstract class Approver {
            protected Approver next;
            Approver setNext(Approver nextApprover) { this.next = nextApprover; return nextApprover; }
            abstract void approve(int amount);
        }
        static class Manager extends Approver {
            @Override
            void approve(int amount) {
                if (amount < 1000) System.out.println("  [Manager] Approved request for $" + amount);
                else if (next != null) next.approve(amount);
            }
        }
        static class Director extends Approver {
            @Override
            void approve(int amount) {
                if (amount < 10000) System.out.println("  [Director] Approved request for $" + amount);
                else if (next != null) next.approve(amount);
            }
        }

        // --- 14. Command ---
        interface Command { void execute(); void undo(); }
        static class TextEditor {
            StringBuilder text = new StringBuilder();
            void insert(int pos, String s) { text.insert(pos, s); }
            void delete(int pos, int len) { text.delete(pos, pos + len); }
        }
        static class InsertCommand implements Command {
            private final TextEditor editor;
            private final String text;
            InsertCommand(TextEditor ed, String txt) { this.editor = ed; this.text = txt; }
            @Override public void execute() { editor.insert(editor.text.length(), text); }
            @Override public void undo() { editor.delete(editor.text.length() - text.length(), text.length()); }
        }

        // --- 15. Interpreter ---
        interface Expression { int interpret(); }
        static class NumberExpression implements Expression {
            private final int number;
            NumberExpression(int n) { this.number = n; }
            @Override public int interpret() { return number; }
        }
        static class AddExpression implements Expression {
            private final Expression left, right;
            AddExpression(Expression l, Expression r) { this.left = l; this.right = r; }
            @Override public int interpret() { return left.interpret() + right.interpret(); }
        }

        // --- 16. Iterator ---
        interface CollectionIterator<T> { boolean hasNext(); T next(); }
        static class ConcreteCollectionIterator<T> implements CollectionIterator<T> {
            private final List<T> list;
            private int index = 0;
            ConcreteCollectionIterator(List<T> l) { this.list = l; }
            @Override public boolean hasNext() { return index < list.size(); }
            @Override public T next() { return list.get(index++); }
        }

        // --- 17. Mediator ---
        interface ChatMediator { void sendMessage(String msg, User user); void addUser(User user); }
        static abstract class User {
            protected ChatMediator mediator;
            protected String name;
            User(ChatMediator med, String n) { this.mediator = med; this.name = n; }
            abstract void send(String msg);
            abstract void receive(String msg);
        }
        static class ChatUser extends User {
            ChatUser(ChatMediator med, String n) { super(med, n); }
            @Override void send(String msg) {
                System.out.println("  [" + name + "] Sending: " + msg);
                mediator.sendMessage(msg, this);
            }
            @Override void receive(String msg) {
                System.out.println("  [" + name + "] Received: " + msg);
            }
        }
        static class ChatMediatorImpl implements ChatMediator {
            private final List<User> users = new ArrayList<>();
            @Override public void addUser(User u) { users.add(u); }
            @Override
            public void sendMessage(String msg, User sender) {
                for (User u : users) {
                    if (u != sender) u.receive(msg);
                }
            }
        }

        // --- 18. Memento ---
        static class EditorMemento {
            private final String state;
            EditorMemento(String s) { this.state = s; }
            private String getState() { return state; }
        }
        static class EditorOriginator {
            private String state;
            void setState(String s) { this.state = s; }
            String getState() { return state; }
            EditorMemento save() { return new EditorMemento(state); }
            void restore(EditorMemento mem) { this.state = mem.getState(); }
        }

        // --- 19. Observer ---
        interface EventListener { void update(String event, String payload); }
        static class LogListener implements EventListener {
            @Override public void update(String ev, String pl) { System.out.printf("    [Logger] Event '%s' payload: %s%n", ev, pl); }
        }
        static class EmailListener implements EventListener {
            @Override public void update(String ev, String pl) { System.out.printf("    [EmailListener] Mail sent for '%s': %s%n", ev, pl); }
        }
        static class EventManager {
            private final Map<String, List<EventListener>> listeners = new HashMap<>();
            void subscribe(String event, EventListener el) {
                listeners.computeIfAbsent(event, k -> new ArrayList<>()).add(el);
            }
            void notify(String event, String payload) {
                for (EventListener el : listeners.getOrDefault(event, List.of())) {
                    el.update(event, payload);
                }
            }
        }

        // --- 20. State ---
        interface State { void doAction(Context context); }
        static class StartState implements State {
            @Override
            public void doAction(Context ctx) {
                System.out.println("  [State] Starting context...");
                ctx.setState(this);
            }
            @Override public String toString() { return "StartState"; }
        }
        static class StopState implements State {
            @Override
            public void doAction(Context ctx) {
                System.out.println("  [State] Stopping context...");
                ctx.setState(this);
            }
            @Override public String toString() { return "StopState"; }
        }
        static class Context {
            private State state;
            void setState(State s) { this.state = s; }
            State getState() { return state; }
        }

        // --- 21. Strategy ---
        interface SortStrategy { void sort(int[] arr); }
        static class BubbleSortStrategy implements SortStrategy {
            @Override public void sort(int[] arr) { bubbleSort(arr); }
        }
        static class QuickSortStrategy implements SortStrategy {
            @Override public void sort(int[] arr) { quickSort(arr, 0, arr.length - 1); }
        }
        static class SortedList {
            private SortStrategy strategy;
            void setStrategy(SortStrategy s) { this.strategy = s; }
            void performSort(int[] arr) { strategy.sort(arr); }
        }

        // --- 22. Template Method ---
        static abstract class Game {
            abstract void initialize();
            abstract void startPlay();
            abstract void endPlay();
            final void play() {
                initialize();
                startPlay();
                endPlay();
            }
        }
        static class Cricket extends Game {
            @Override void initialize() { System.out.println("    [Cricket] Initializing game setup."); }
            @Override void startPlay() { System.out.println("    [Cricket] Commencing gameplay."); }
            @Override void endPlay() { System.out.println("    [Cricket] Finalizing match results."); }
        }

        // --- 23. Visitor ---
        interface ItemElement { int accept(ShoppingCartVisitor visitor); }
        static class BookItem implements ItemElement {
            private final int price;
            BookItem(int p) { this.price = p; }
            int getPrice() { return price; }
            @Override public int accept(ShoppingCartVisitor visitor) { return visitor.visit(this); }
        }
        interface ShoppingCartVisitor { int visit(BookItem book); }
        static class ShoppingCartVisitorImpl implements ShoppingCartVisitor {
            @Override public int visit(BookItem book) {
                System.out.println("    [Visitor] Visited Book, price: " + book.getPrice());
                return book.getPrice();
            }
        }

        static void designPatternsDemo() {
            System.out.println("\n" + "=".repeat(60));
            System.out.println("4.  DESIGN PATTERNS DEMO (ALL 23 GOF PATTERNS)");
            System.out.println("=".repeat(60));

            // Creational Demos
            System.out.println("  --- Creational Patterns ---");
            DatabaseConnection db1 = DatabaseConnection.getInstance();
            DatabaseConnection db2 = DatabaseConnection.getInstance();
            System.out.println("  Singleton identity match: " + (db1 == db2));

            NotificationFactory factory = new EmailNotificationFactory();
            factory.sendNotification();

            GUIFactory winFactory = new WinFactory();
            Button winBtn = winFactory.createButton();
            winBtn.paint();

            HttpRequest request = new HttpRequest.Builder()
                .url("https://api.example.com/v1")
                .method("POST")
                .header("Authorization", "Bearer token_xyz")
                .body("{'id':123}")
                .build();
            System.out.println("  Builder Request: " + request);

            ShapePrototype cloneCircle = (CirclePrototype) new CirclePrototype().clone();
            cloneCircle.draw();

            // Structural Demos
            System.out.println("\n  --- Structural Patterns ---");
            LegacyPrinter lp = new LegacyPrinter();
            ModernPrinter mp = new PrinterAdapter(lp);
            mp.printNew("Adapter wraps legacy printer logic.");

            ShapeBridge redCircle = new CircleBridge(100, 100, 10, new RedCircle());
            redCircle.draw();

            CompositeGraphic rootComposite = new CompositeGraphic();
            rootComposite.add(new LeafGraphic("Button"));
            rootComposite.add(new LeafGraphic("TextField"));
            rootComposite.print();

            DataSource fileDS = new FileDataSource();
            DataSource encryptedDS = new EncryptionDecorator(fileDS);
            encryptedDS.writeData("Hello World Secret");
            System.out.println("  Decorator Encrypted:  " + fileDS.readData());
            System.out.println("  Decorator Decrypted:  " + encryptedDS.readData());

            ComputerFacade computer = new ComputerFacade();
            computer.start();

            FlyweightFactory fwFactory = new FlyweightFactory();
            fwFactory.getFlyweight("Key1").operation(10);
            fwFactory.getFlyweight("Key1").operation(20);

            Image proxyImage = new ProxyImage("photo.png");
            proxyImage.display();

            // Behavioral Demos
            System.out.println("\n  --- Behavioral Patterns ---");
            Approver mgr = new Manager();
            Approver dir = new Director();
            mgr.setNext(dir);
            mgr.approve(500);
            mgr.approve(5000);

            TextEditor ed = new TextEditor();
            Command insCmd = new InsertCommand(ed, "Hello Command!");
            insCmd.execute();
            System.out.println("  Command text: " + ed.text);
            insCmd.undo();
            System.out.println("  Command undone text: " + ed.text);

            Expression sum = new AddExpression(new NumberExpression(10), new NumberExpression(20));
            System.out.println("  Interpreter (10 + 20) = " + sum.interpret());

            List<String> coll = List.of("One", "Two", "Three");
            CollectionIterator<String> it = new ConcreteCollectionIterator<>(coll);
            System.out.print("  Iterator elements: ");
            while (it.hasNext()) System.out.print(it.next() + " ");
            System.out.println();

            ChatMediator chatroom = new ChatMediatorImpl();
            User user1 = new ChatUser(chatroom, "User1");
            User user2 = new ChatUser(chatroom, "User2");
            chatroom.addUser(user1);
            chatroom.addUser(user2);
            user1.send("Hello Room");

            EditorOriginator orig = new EditorOriginator();
            orig.setState("State1");
            EditorMemento mem = orig.save();
            orig.setState("State2");
            System.out.println("  Originator State: " + orig.getState());
            orig.restore(mem);
            System.out.println("  Originator Restored: " + orig.getState());

            EventManager eventMgr = new EventManager();
            eventMgr.subscribe("Save", new LogListener());
            eventMgr.subscribe("Save", new EmailListener());
            eventMgr.notify("Save", "Document1.txt");

            Context stateCtx = new Context();
            new StartState().doAction(stateCtx);
            new StopState().doAction(stateCtx);

            SortedList listToSort = new SortedList();
            listToSort.setStrategy(new QuickSortStrategy());
            int[] sortData = {5, 2, 8, 1};
            listToSort.performSort(sortData);
            System.out.println("  Strategy QuickSort: " + Arrays.toString(sortData));

            Game game = new Cricket();
            game.play();

            ItemElement book = new BookItem(15);
            ShoppingCartVisitor cartVisitor = new ShoppingCartVisitorImpl();
            book.accept(cartVisitor);
        }
"""
