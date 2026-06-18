# cpp_chunk4.py
# Phase 4: All 23 Gang of Four (GoF) Design Patterns in Modern C++ (Expanded)

chunk_content = r"""
    /* ==================================================================
     *  PHASE 4: 23 GANG OF FOUR DESIGN PATTERNS IN MODERN C++
     * ================================================================== */

    /* --- CREATIONAL PATTERNS --- */

    // 1. Singleton (Meyers Singleton)
    class Singleton {
    public:
        static Singleton& get_instance() {
            static Singleton instance;
            return instance;
        }
        void run() const { cout << "      [Singleton] Active.\n"; }
    private:
        Singleton() = default;
        Singleton(const Singleton&) = delete;
        Singleton& operator=(const Singleton&) = delete;
    };

    // 2. Factory Method
    struct Product {
        virtual ~Product() = default;
        virtual string name() const = 0;
    };
    struct ConcreteProductA : public Product {
        string name() const override { return "ProductA"; }
    };
    struct Creator {
        virtual ~Creator() = default;
        virtual unique_ptr<Product> create() const = 0;
    };
    struct ConcreteCreatorA : public Creator {
        unique_ptr<Product> create() const override {
            return make_unique<ConcreteProductA>();
        }
    };

    // 3. Abstract Factory
    struct AbstractButton {
        virtual ~AbstractButton() = default;
        virtual void paint() const = 0;
    };
    struct WinButton : public AbstractButton {
        void paint() const override { cout << "      [Abstract Factory] Painting WinButton.\n"; }
    };
    struct OSXButton : public AbstractButton {
        void paint() const override { cout << "      [Abstract Factory] Painting OSXButton.\n"; }
    };
    struct GUIFactory {
        virtual ~GUIFactory() = default;
        virtual unique_ptr<AbstractButton> create_button() const = 0;
    };
    struct WinFactory : public GUIFactory {
        unique_ptr<AbstractButton> create_button() const override { return make_unique<WinButton>(); }
    };
    struct OSXFactory : public GUIFactory {
        unique_ptr<AbstractButton> create_button() const override { return make_unique<OSXButton>(); }
    };

    // 4. Builder
    class PC {
    public:
        string cpu;
        string ram;
        string storage;
        void print() const {
            cout << "      [Builder] PC: CPU=" << cpu << ", RAM=" << ram << ", Storage=" << storage << "\n";
        }
    };
    class PCBuilder {
        PC pc;
    public:
        PCBuilder& add_cpu(string cpu) { pc.cpu = move(cpu); return *this; }
        PCBuilder& add_ram(string ram) { pc.ram = move(ram); return *this; }
        PCBuilder& add_storage(string storage) { pc.storage = move(storage); return *this; }
        PC build() { return move(pc); }
    };

    // 5. Prototype
    struct Prototype {
        virtual ~Prototype() = default;
        virtual unique_ptr<Prototype> clone() const = 0;
        virtual void print() const = 0;
    };
    class ConcretePrototype : public Prototype {
        int id;
    public:
        ConcretePrototype(int i) : id(i) {}
        unique_ptr<Prototype> clone() const override { return make_unique<ConcretePrototype>(id); }
        void print() const override { cout << "      [Prototype] ConcretePrototype id=" << id << "\n"; }
    };

    /* --- STRUCTURAL PATTERNS --- */

    // 6. Adapter
    class Target {
    public:
        virtual ~Target() = default;
        virtual void request() const = 0;
    };
    class Adaptee {
    public:
        void specific_request() const { cout << "      [Adapter] Adaptee specific request.\n"; }
    };
    class Adapter : public Target {
        unique_ptr<Adaptee> adaptee;
    public:
        Adapter() : adaptee(make_unique<Adaptee>()) {}
        void request() const override { adaptee->specific_request(); }
    };

    // 7. Bridge
    struct Implementor {
        virtual ~Implementor() = default;
        virtual void draw_impl() const = 0;
    };
    struct RedCircleImpl : public Implementor {
        void draw_impl() const override { cout << "      [Bridge] Drawing Red Circle.\n"; }
    };
    struct Abstraction {
    protected:
        shared_ptr<Implementor> impl;
    public:
        Abstraction(shared_ptr<Implementor> im) : impl(move(im)) {}
        virtual ~Abstraction() = default;
        virtual void draw() const = 0;
    };
    class RefinedAbstraction : public Abstraction {
    public:
        RefinedAbstraction(shared_ptr<Implementor> im) : Abstraction(move(im)) {}
        void draw() const override { impl->draw_impl(); }
    };

    // 8. Composite
    struct Component {
        virtual ~Component() = default;
        virtual void operation() const = 0;
    };
    class Leaf : public Component {
    public:
        void operation() const override { cout << "        Leaf operation.\n"; }
    };
    class Composite : public Component {
        vector<shared_ptr<Component>> children;
    public:
        void add(shared_ptr<Component> child) { children.push_back(move(child)); }
        void operation() const override {
            cout << "      [Composite] Composite operation:\n";
            for (const auto& c : children) c->operation();
        }
    };

    // 9. Decorator
    struct Window {
        virtual ~Window() = default;
        virtual void draw() const = 0;
    };
    class SimpleWindow : public Window {
    public:
        void draw() const override { cout << "      SimpleWindow"; }
    };
    class WindowDecorator : public Window {
    protected:
        unique_ptr<Window> w;
    public:
        WindowDecorator(unique_ptr<Window> win) : w(move(win)) {}
    };
    class ScrollbarWindowDecorator : public WindowDecorator {
    public:
        ScrollbarWindowDecorator(unique_ptr<Window> win) : WindowDecorator(move(win)) {}
        void draw() const override { w->draw(); cout << " + scrollbar"; }
    };

    // 10. Facade
    class SubsystemA {
    public:
        void startup() const { cout << "        SubsystemA online.\n"; }
    };
    class SubsystemB {
    public:
        void run() const { cout << "        SubsystemB running.\n"; }
    };
    class Facade {
        SubsystemA a;
        SubsystemB b;
    public:
        void run_all() const {
            cout << "      [Facade] Initializing all subsystems:\n";
            a.startup();
            b.run();
        }
    };

    // 11. Flyweight
    class Flyweight {
        string intrinsic_state;
    public:
        Flyweight(string s) : intrinsic_state(move(s)) {}
        void operation(int extrinsic_state) const {
            cout << "      [Flyweight] Intrinsic: " << intrinsic_state << ", Extrinsic: " << extrinsic_state << "\n";
        }
    };
    class FlyweightFactory {
        unordered_map<string, shared_ptr<Flyweight>> cache;
    public:
        shared_ptr<Flyweight> get_flyweight(const string& key) {
            if (cache.find(key) == cache.end()) {
                cache[key] = make_shared<Flyweight>(key);
            }
            return cache[key];
        }
    };

    // 12. Proxy
    struct SubjectInterface {
        virtual ~SubjectInterface() = default;
        virtual void request() const = 0;
    };
    class RealSubject : public SubjectInterface {
    public:
        void request() const override { cout << "      [Proxy] RealSubject executing request.\n"; }
    };
    class Proxy : public SubjectInterface {
        unique_ptr<RealSubject> real_subject;
    public:
        Proxy() : real_subject(make_unique<RealSubject>()) {}
        void request() const override {
            cout << "      [Proxy] Logger proxy logging before execution:\n";
            real_subject->request();
        }
    };

    /* --- BEHAVIORAL PATTERNS --- */

    // 13. Chain of Responsibility
    class Handler {
    protected:
        unique_ptr<Handler> next_handler;
    public:
        virtual ~Handler() = default;
        void set_next(unique_ptr<Handler> handler) { next_handler = move(handler); }
        virtual void handle(int request) const {
            if (next_handler) next_handler->handle(request);
        }
    };
    class ConcreteHandlerA : public Handler {
    public:
        void handle(int request) const override {
            if (request < 10) {
                cout << "      [Chain of Responsibility] Handled by HandlerA (request=" << request << ")\n";
            } else {
                Handler::handle(request);
            }
        }
    };
    class ConcreteHandlerB : public Handler {
    public:
        void handle(int request) const override {
            if (request >= 10) {
                cout << "      [Chain of Responsibility] Handled by HandlerB (request=" << request << ")\n";
            } else {
                Handler::handle(request);
            }
        }
    };

    // 14. Command with Undo/Redo & History stacks
    struct Receiver {
        void action_on() const { cout << "      [Command] Receiver light ON.\n"; }
        void action_off() const { cout << "      [Command] Receiver light OFF.\n"; }
    };
    struct Command {
        virtual ~Command() = default;
        virtual void execute() const = 0;
        virtual void undo() const = 0;
    };
    class OnCommand : public Command {
        shared_ptr<Receiver> recv;
    public:
        OnCommand(shared_ptr<Receiver> r) : recv(move(r)) {}
        void execute() const override { recv->action_on(); }
        void undo() const override { recv->action_off(); }
    };
    class OffCommand : public Command {
        shared_ptr<Receiver> recv;
    public:
        OffCommand(shared_ptr<Receiver> r) : recv(move(r)) {}
        void execute() const override { recv->action_off(); }
        void undo() const override { recv->action_on(); }
    };
    class RemoteControl {
    private:
        mutable stack<shared_ptr<Command>> undo_stack;
        mutable stack<shared_ptr<Command>> redo_stack;
    public:
        void submit(const shared_ptr<Command>& cmd) {
            cmd->execute();
            undo_stack.push(cmd);
            while (!redo_stack.empty()) redo_stack.pop(); // Clear redo on new command
        }
        void undo() const {
            if (undo_stack.empty()) return;
            auto cmd = undo_stack.top();
            undo_stack.pop();
            cmd->undo();
            redo_stack.push(cmd);
        }
        void redo() const {
            if (redo_stack.empty()) return;
            auto cmd = redo_stack.top();
            redo_stack.pop();
            cmd->execute();
            undo_stack.push(cmd);
        }
    };

    // 15. Interpreter (Add, Sub, Mul)
    struct ExpNode {
        virtual ~ExpNode() = default;
        virtual int interpret() const = 0;
    };
    class NumberExp : public ExpNode {
        int val;
    public:
        NumberExp(int v) : val(v) {}
        int interpret() const override { return val; }
    };
    class AddExp : public ExpNode {
        unique_ptr<ExpNode> left, right;
    public:
        AddExp(unique_ptr<ExpNode> l, unique_ptr<ExpNode> r) : left(move(l)), right(move(r)) {}
        int interpret() const override { return left->interpret() + right->interpret(); }
    };
    class SubExp : public ExpNode {
        unique_ptr<ExpNode> left, right;
    public:
        SubExp(unique_ptr<ExpNode> l, unique_ptr<ExpNode> r) : left(move(l)), right(move(r)) {}
        int interpret() const override { return left->interpret() - right->interpret(); }
    };
    class MulExp : public ExpNode {
        unique_ptr<ExpNode> left, right;
    public:
        MulExp(unique_ptr<ExpNode> l, unique_ptr<ExpNode> r) : left(move(l)), right(move(r)) {}
        int interpret() const override { return left->interpret() * right->interpret(); }
    };

    // 16. Iterator
    template <typename T>
    class SimpleContainer {
        vector<T> items;
    public:
        void add(T item) { items.push_back(move(item)); }
        class Iterator {
            const vector<T>& ref;
            size_t pos = 0;
        public:
            Iterator(const vector<T>& r, size_t p = 0) : ref(r), pos(p) {}
            bool has_next() const { return pos < ref.size(); }
            T next() { return ref[pos++]; }
        };
        Iterator get_iterator() const { return Iterator(items); }
    };

    // 17. Mediator
    struct Colleague;
    struct Mediator {
        virtual ~Mediator() = default;
        virtual void notify(Colleague* sender, const string& msg) = 0;
    };
    struct Colleague {
    protected:
        Mediator* med;
    public:
        Colleague(Mediator* m) : med(m) {}
        virtual ~Colleague() = default;
        virtual void receive(const string& msg) = 0;
    };
    class ConcreteColleague : public Colleague {
        string name;
    public:
        ConcreteColleague(Mediator* m, string n) : Colleague(m), name(move(n)) {}
        void send(const string& msg) { med->notify(this, msg); }
        void receive(const string& msg) override {
            cout << "      [Mediator] Participant " << name << " received: " << msg << "\n";
        }
    };
    class ChatRoomMediator : public Mediator {
    public:
        vector<ConcreteColleague*> members;
        void notify(Colleague* sender, const string& msg) override {
            for (auto* m : members) {
                if (m != sender) m->receive(msg);
            }
        }
    };

    // 18. Memento with Caretaker stack
    class Memento {
        string state;
    public:
        Memento(string s) : state(move(s)) {}
        string get_state() const { return state; }
    };
    class Originator {
        string state;
    public:
        void set_state(string s) { state = move(s); }
        string get_state() const { return state; }
        Memento save() { return Memento(state); }
        void restore(const Memento& m) { state = m.get_state(); }
    };
    class Caretaker {
    private:
        stack<Memento> history;
    public:
        void save_state(Originator& o) { history.push(o.save()); }
        void undo(Originator& o) {
            if (history.empty()) return;
            o.restore(history.top());
            history.pop();
        }
    };

    // 19. Observer
    struct CXXObserver {
        virtual ~CXXObserver() = default;
        virtual void update(int state) = 0;
    };
    class CXXConcreteObserver : public CXXObserver {
        string name;
    public:
        CXXConcreteObserver(string n) : name(move(n)) {}
        void update(int state) override {
            cout << "      [Observer " << name << "] Notified state changed to: " << state << "\n";
        }
    };
    class CXXSubject {
        vector<shared_ptr<CXXObserver>> observers;
        int state = 0;
    public:
        void attach(shared_ptr<CXXObserver> obs) { observers.push_back(move(obs)); }
        void set_state(int s) {
            state = s;
            for (const auto& obs : observers) obs->update(state);
        }
    };

    // 20. State Pattern with 3 concrete states (A, B, C)
    struct StatePatternContext;
    struct State {
        virtual ~State() = default;
        virtual void handle(StatePatternContext& ctx) = 0;
    };
    struct StatePatternContext {
        unique_ptr<State> current_state;
        StatePatternContext(unique_ptr<State> init) : current_state(move(init)) {}
        void request() { current_state->handle(*this); }
    };
    struct ConcreteStateC : public State {
        void handle(StatePatternContext& ctx);
    };
    struct ConcreteStateB : public State {
        void handle(StatePatternContext& ctx) override {
            cout << "      [State] State B transitioning to State C...\n";
            ctx.current_state = make_unique<ConcreteStateC>();
        }
    };
    struct ConcreteStateA : public State {
        void handle(StatePatternContext& ctx) override {
            cout << "      [State] State A transitioning to State B...\n";
            ctx.current_state = make_unique<ConcreteStateB>();
        }
    };
    void ConcreteStateC::handle(StatePatternContext& ctx) {
        cout << "      [State] State C transitioning back to State A...\n";
        ctx.current_state = make_unique<ConcreteStateA>();
    }

    // 21. Strategy
    struct SortingStrategy {
        virtual ~SortingStrategy() = default;
        virtual void sort(vector<int>& arr) = 0;
    };
    struct BubbleSortStrategy : public SortingStrategy {
        void sort(vector<int>& arr) override {
            int n = arr.size();
            for (int i = 0; i < n - 1; i++) {
                for (int j = 0; j < n - i - 1; j++) {
                    if (arr[j] > arr[j+1]) swap(arr[j], arr[j+1]);
                }
            }
        }
    };

    // 22. Template Method
    class Game {
    protected:
        virtual void initialize() = 0;
        virtual void start_play() = 0;
        virtual void end_play() = 0;
    public:
        virtual ~Game() = default;
        void play() {
            initialize();
            start_play();
            end_play();
        }
    };
    class Football : public Game {
    protected:
        void initialize() override { cout << "      [Template Method] Football Init.\n"; }
        void start_play() override { cout << "      [Template Method] Football Started.\n"; }
        void end_play() override { cout << "      [Template Method] Football Finished.\n"; }
    };

    // 23. Visitor double-dispatch (Concrete elements A & B)
    struct Visitor;
    struct Element {
        virtual ~Element() = default;
        virtual void accept(Visitor& v) = 0;
    };
    struct ConcreteElementA : public Element {
        int val = 999;
        void accept(Visitor& v) override;
    };
    struct ConcreteElementB : public Element {
        string text = "VisitorElementB";
        void accept(Visitor& v) override;
    };
    struct Visitor {
        virtual ~Visitor() = default;
        virtual void visit(ConcreteElementA& el) = 0;
        virtual void visit(ConcreteElementB& el) = 0;
    };
    void ConcreteElementA::accept(Visitor& v) { v.visit(*this); }
    void ConcreteElementB::accept(Visitor& v) { v.visit(*this); }

    struct ConcreteVisitor : public Visitor {
        void visit(ConcreteElementA& el) override {
            cout << "      [Visitor] Visited ElementA with value: " << el.val << "\n";
        }
        void visit(ConcreteElementB& el) override {
            cout << "      [Visitor] Visited ElementB with text: '" << el.text << "'\n";
        }
    };

    static void design_patterns_demo() {
        print_sep("PHASE 4: 23 GoF DESIGN PATTERNS IN MODERN C++");

        // 1. Singleton
        Singleton::get_instance().run();

        // 2. Factory Method
        unique_ptr<Creator> creator = make_unique<ConcreteCreatorA>();
        unique_ptr<Product> prod = creator->create();
        cout << "      [Factory Method] Created product: " << prod->name() << "\n";

        // 3. Abstract Factory
        unique_ptr<GUIFactory> factory = make_unique<WinFactory>();
        unique_ptr<AbstractButton> btn = factory->create_button();
        btn->paint();

        // 4. Builder
        PC pc = PCBuilder().add_cpu("AMD Ryzen 9").add_ram("32GB").add_storage("2TB NVMe").build();
        pc.print();

        // 5. Prototype
        unique_ptr<Prototype> p1 = make_unique<ConcretePrototype>(42);
        unique_ptr<Prototype> p2 = p1->clone();
        p2->print();

        // 6. Adapter
        unique_ptr<Target> target = make_unique<Adapter>();
        target->request();

        // 7. Bridge
        auto bridge_impl = make_shared<RedCircleImpl>();
        RefinedAbstraction bridge_abs(bridge_impl);
        bridge_abs.draw();

        // 8. Composite
        auto comp_root = make_shared<Composite>();
        comp_root->add(make_shared<Leaf>());
        comp_root->add(make_shared<Leaf>());
        comp_root->operation();

        // 9. Decorator
        unique_ptr<Window> w = make_unique<SimpleWindow>();
        w = make_unique<ScrollbarWindowDecorator>(move(w));
        cout << "      [Decorator] Drawing window: ";
        w->draw();
        cout << "\n";

        // 10. Facade
        Facade facade;
        facade.run_all();

        // 11. Flyweight
        FlyweightFactory flyweight_fac;
        auto fw1 = flyweight_fac.get_flyweight("FlyweightA");
        fw1->operation(100);

        // 12. Proxy
        unique_ptr<SubjectInterface> proxy = make_unique<Proxy>();
        proxy->request();

        // 13. Chain of Responsibility
        auto h1 = make_unique<ConcreteHandlerA>();
        auto h2 = make_unique<ConcreteHandlerB>();
        h1->set_next(move(h2));
        h1->handle(5);
        h1->handle(15);

        // 14. Command with Undo/Redo
        auto light = make_shared<Receiver>();
        auto cmd_on = make_shared<OnCommand>(light);
        RemoteControl remote;
        cout << "      [Command] Submitting OnCommand...\n";
        remote.submit(cmd_on);
        cout << "      [Command] Undoing last command...\n";
        remote.undo();
        cout << "      [Command] Redoing last command...\n";
        remote.redo();

        // 15. Interpreter
        unique_ptr<ExpNode> expr = make_unique<AddExp>(
            make_unique<SubExp>(make_unique<NumberExp>(100), make_unique<NumberExp>(20)),
            make_unique<MulExp>(make_unique<NumberExp>(5), make_unique<NumberExp>(4))
        );
        cout << "      [Interpreter] ((100 - 20) + (5 * 4)) = " << expr->interpret() << "\n";

        // 16. Iterator
        SimpleContainer<int> cont;
        cont.add(10);
        cont.add(20);
        cont.add(30);
        auto it = cont.get_iterator();
        cout << "      [Iterator] Listing elements: ";
        while (it.has_next()) {
            cout << it.next() << " ";
        }
        cout << "\n";

        // 17. Mediator
        ChatRoomMediator chat;
        ConcreteColleague user1(&chat, "User1");
        ConcreteColleague user2(&chat, "User2");
        chat.members.push_back(&user1);
        chat.members.push_back(&user2);
        user1.send("Hello World");

        // 18. Memento with Caretaker
        Originator orig;
        Caretaker caretaker;
        orig.set_state("State1");
        caretaker.save_state(orig);
        orig.set_state("State2");
        cout << "      [Memento] Current state: " << orig.get_state() << "\n";
        caretaker.undo(orig);
        cout << "      [Memento] Restored state: " << orig.get_state() << "\n";

        // 19. Observer
        auto sub = make_shared<CXXSubject>();
        auto o1 = make_shared<CXXConcreteObserver>("Obs1");
        sub->attach(o1);
        sub->set_state(100);

        // 20. State transitions A -> B -> C -> A
        StatePatternContext state_ctx(make_unique<ConcreteStateA>());
        state_ctx.request();
        state_ctx.request();
        state_ctx.request();

        // 21. Strategy
        vector<int> sort_nums = {5, 2, 9, 1, 6};
        BubbleSortStrategy bubble_strat;
        bubble_strat.sort(sort_nums);
        cout << "      [Strategy] Bubble Sorted: ";
        for (int x : sort_nums) cout << x << " ";
        cout << "\n";

        // 22. Template Method
        Football football;
        football.play();

        // 23. Visitor double-dispatch
        ConcreteElementA elA;
        ConcreteElementB elB;
        ConcreteVisitor visitor;
        elA.accept(visitor);
        elB.accept(visitor);
    }
"""
