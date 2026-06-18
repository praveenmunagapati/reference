# append_chunk2.py
# Appends Phase 4 (23 GoF Design Patterns) section to build_cs_ds_encyclopedia_c.py

import os

c_quote = "'''"

chunk_content = r"""
# ---------------------------------------------------------------------------
# PHASE 4: DESIGN PATTERNS CATALOG IN C (ALL 23 GoF PATTERNS)
# ---------------------------------------------------------------------------
add_section("PHASE_4_DESIGN_PATTERNS", r{c_quote}
/* ==================================================================
 *  PHASE 4: DESIGN PATTERNS CATALOG IN C (ALL 23 GoF PATTERNS)
 * ================================================================== */

/* 4.1 Creational Patterns: Singleton, Factory Method, Abstract Factory, Builder, Prototype */

/* Singleton */
typedef struct {
    int data;
} Singleton;

static Singleton *singleton_get_instance(void) {
    static Singleton instance = {42};
    return &instance;
}

/* Factory Method */
typedef struct Product {
    void (*use)(void);
} Product;

static void concrete_product_use(void) {
    printf("    [Factory Method] Using Concrete Product.\n");
}

static Product *factory_create_product(void) {
    static Product p = { concrete_product_use };
    return &p;
}

/* Abstract Factory */
typedef struct AbstractButton {
    void (*paint)(void);
} AbstractButton;

typedef struct AbstractCheckbox {
    void (*toggle)(void);
} AbstractCheckbox;

typedef struct AbstractFactory {
    AbstractButton* (*create_button)(void);
    AbstractCheckbox* (*create_checkbox)(void);
} AbstractFactory;

static void win_button_paint(void) { printf("    [Abstract Factory] Painting Windows Button.\n"); }
static void win_checkbox_toggle(void) { printf("    [Abstract Factory] Toggling Windows Checkbox.\n"); }
static AbstractButton win_button = { win_button_paint };
static AbstractCheckbox win_checkbox = { win_checkbox_toggle };

static AbstractButton* win_factory_create_button(void) { return &win_button; }
static AbstractCheckbox* win_factory_create_checkbox(void) { return &win_checkbox; }
static AbstractFactory win_factory = { win_factory_create_button, win_factory_create_checkbox };

/* Builder */
typedef struct {
    char cpu[32];
    char ram[32];
    char storage[32];
} ComputerProduct;

typedef struct {
    ComputerProduct product;
    void (*set_cpu)(ComputerProduct*, const char*);
    void (*set_ram)(ComputerProduct*, const char*);
} ComputerBuilder;

static void builder_set_cpu(ComputerProduct *p, const char *cpu) { strcpy(p->cpu, cpu); }
static void builder_set_ram(ComputerProduct *p, const char *ram) { strcpy(p->ram, ram); }

/* Prototype */
typedef struct ProtoShape {
    struct ProtoShape* (*clone)(const struct ProtoShape *self);
    int id;
} ProtoShape;

static ProtoShape* clone_shape(const ProtoShape *self) {
    ProtoShape *copy = (ProtoShape*)malloc(sizeof(ProtoShape));
    copy->clone = self->clone;
    copy->id = self->id;
    return copy;
}

/* 4.2 Structural Patterns: Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy */

/* Adapter */
typedef struct TargetInterface {
    void (*request)(void);
} TargetInterface;

typedef struct Adaptee {
    void (*specific_request)(void);
} Adaptee;

static void adaptee_specific_request(void) {
    printf("    [Adapter] Specific request on Adaptee called.\n");
}

typedef struct {
    TargetInterface base;
    Adaptee *adaptee;
} Adapter;

static void adapter_request(void) {
    static Adaptee temp_adaptee = { adaptee_specific_request };
    temp_adaptee.specific_request();
}

/* Bridge */
typedef struct DeviceImplementor {
    void (*turn_on)(void);
} DeviceImplementor;

typedef struct RemoteControl {
    DeviceImplementor *impl;
    void (*toggle_power)(struct RemoteControl *self);
} RemoteControl;

static void tv_turn_on(void) { printf("    [Bridge] TV turn on.\n"); }
static DeviceImplementor tv_impl = { tv_turn_on };

static void remote_toggle_power(RemoteControl *self) {
    self->impl->turn_on();
}

/* Composite */
typedef struct GraphicComponent {
    void (*draw)(struct GraphicComponent *self);
    struct GraphicComponent *children[4];
    int child_count;
} GraphicComponent;

static void leaf_draw(GraphicComponent *self) {
    (void)self;
    printf("      [Composite] Drawing Leaf Component.\n");
}

static void composite_draw(GraphicComponent *self) {
    printf("      [Composite] Drawing Composite:\n");
    for (int i = 0; i < self->child_count; i++) {
        self->children[i]->draw(self->children[i]);
    }
}

/* Decorator */
typedef struct Coffee {
    double (*cost)(void);
} Coffee;

static double simple_coffee_cost(void) { return 2.0; }

typedef struct MilkDecorator {
    Coffee base;
    Coffee *coffee_to_decorate;
} MilkDecorator;

static double milk_coffee_cost(void) { return simple_coffee_cost() + 0.5; }

/* Facade */
typedef struct { void (*init)(void); } FacadeSubsystemA;
typedef struct { void (*start)(void); } FacadeSubsystemB;

static void facade_sub_a_init(void) { printf("    [Facade] Subsystem A initialized.\n"); }
static void facade_sub_b_start(void) { printf("    [Facade] Subsystem B started.\n"); }

typedef struct {
    FacadeSubsystemA a;
    FacadeSubsystemB b;
    void (*run)(void);
} SystemFacade;

static void facade_run(void) {
    FacadeSubsystemA sa = { facade_sub_a_init };
    FacadeSubsystemB sb = { facade_sub_b_start };
    sa.init();
    sb.start();
}

/* Flyweight */
typedef struct {
    char key; // Intrinsic state (shared)
} CharacterFlyweight;

static void flyweight_print(const CharacterFlyweight *f, int size) {
    printf("    [Flyweight] Intrinsic key '%c' with Extrinsic font size: %d\n", f->key, size);
}

/* Proxy */
typedef struct RealSubject {
    void (*request)(void);
} RealSubject;

static void real_subject_request(void) {
    printf("    [Proxy] Real subject request executed.\n");
}

typedef struct {
    RealSubject base;
    RealSubject *real;
} ProxySubject;

static void proxy_request(void) {
    static RealSubject r = { real_subject_request };
    printf("    [Proxy] Logging access via proxy.\n");
    r.request();
}

/* 4.3 Behavioral Patterns: Chain of Responsibility, Command, Interpreter, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor */

/* Chain of Responsibility */
typedef struct RequestHandler {
    struct RequestHandler *next;
    void (*handle)(struct RequestHandler *self, int level);
} RequestHandler;

static void concrete_handler_handle(RequestHandler *self, int level) {
    if (level < 5) {
        printf("    [Chain of Responsibility] Request handled by base handler.\n");
    } else if (self->next) {
        self->next->handle(self->next, level);
    }
}

/* Command */
typedef struct CommandObj {
    void (*execute)(void);
} CommandObj;

static void light_on_execute(void) {
    printf("    [Command] Light turned ON.\n");
}

/* Interpreter */
typedef struct Expression {
    int (*interpret)(struct Expression *self);
    int val;
} Expression;

static int int_interpret(Expression *self) { return self->val; }

/* Iterator */
typedef struct VectorIterator {
    int *data;
    int size;
    int index;
    bool (*has_next)(struct VectorIterator *self);
    int (*next)(struct VectorIterator *self);
} VectorIterator;

static bool iter_has_next(VectorIterator *self) { return self->index < self->size; }
static int iter_next(VectorIterator *self) { return self->data[self->index++]; }

/* Mediator */
typedef struct Participant {
    char name[32];
    void (*receive)(struct Participant *self, const char *msg);
} Participant;

static void participant_receive(Participant *self, const char *msg) {
    printf("    [Mediator] Participant %s received message: %s\n", self->name, msg);
}

typedef struct ChatMediator {
    Participant *p1;
    Participant *p2;
    void (*send)(struct ChatMediator *self, const char *msg, Participant *sender);
} ChatMediator;

static void chat_mediator_send(struct ChatMediator *self, const char *msg, Participant *sender) {
    if (sender == self->p1) self->p2->receive(self->p2, msg);
    else self->p1->receive(self->p1, msg);
}

/* Memento */
typedef struct {
    int state;
} StateMemento;

typedef struct {
    int state;
    StateMemento (*save)(int);
    void (*restore)(int*, StateMemento);
} EditorOriginator;

static StateMemento originator_save(int val) {
    StateMemento m = { val };
    return m;
}
static void originator_restore(int *state, StateMemento m) {
    *state = m.state;
}

/* Observer */
typedef struct Observer {
    void (*update)(struct Observer *self, int val);
} Observer;

static void obs_update(Observer *self, int val) {
    (void)self;
    printf("    [Observer] Notified with updated state value: %d\n", val);
}

typedef struct {
    Observer *observers[2];
    int count;
    int val;
    void (*register_obs)(Observer*);
    void (*notify)(int);
} SubjectNotifier;

/* State */
typedef struct ConnectionState {
    void (*handle)(void);
} ConnectionState;

static void state_connected(void) { printf("    [State] Connection State: Connected.\n"); }
static void state_disconnected(void) { printf("    [State] Connection State: Disconnected.\n"); }

/* Strategy */
typedef struct SortStrategy {
    void (*sort)(int arr[], int n);
} SortStrategy;

static void bubble_sort_strategy(int arr[], int n) {
    for (int i = 0; i < n-1; i++) {
        for (int j = 0; j < n-i-1; j++) {
            if (arr[j] > arr[j+1]) swap_ints(&arr[j], &arr[j+1]);
        }
    }
}

/* Template Method */
typedef struct GameAlgorithm {
    void (*initialize)(void);
    void (*start_play)(void);
    void (*end_play)(void);
    void (*play)(struct GameAlgorithm *self);
} GameAlgorithm;

static void game_play(GameAlgorithm *self) {
    self->initialize();
    self->start_play();
    self->end_play();
}

/* Visitor */
typedef struct VisitorElement VisitorElement;
typedef struct ElementVisitor {
    void (*visit)(struct ElementVisitor *self, VisitorElement *e);
} ElementVisitor;

typedef struct VisitorElement {
    int value;
    void (*accept)(struct VisitorElement *self, ElementVisitor *v);
} VisitorElement;

static void concrete_visitor_visit(ElementVisitor *self, VisitorElement *e) {
    (void)self;
    printf("    [Visitor] Visited Element with internal value: %d\n", e->value);
}

static void element_accept(VisitorElement *self, ElementVisitor *v) {
    v->visit(v, self);
}

static void design_patterns_demo(void) {
    print_sep("PHASE 4: 23 GoF DESIGN PATTERNS IN C");

    /* Singleton */
    Singleton *s = singleton_get_instance();
    printf("  Singleton state value: %d\n", s->data);

    /* Factory Method */
    Product *p = factory_create_product();
    p->use();

    /* Abstract Factory */
    AbstractButton *btn = win_factory.create_button();
    AbstractCheckbox *cb = win_factory.create_checkbox();
    btn->paint();
    cb->toggle();

    /* Builder */
    ComputerBuilder builder;
    builder.set_cpu = builder_set_cpu;
    builder.set_ram = builder_set_ram;
    builder.set_cpu(&builder.product, "Intel Core i9");
    builder.set_ram(&builder.product, "64GB DDR5");
    printf("  Computer built: CPU=%s, RAM=%s\n", builder.product.cpu, builder.product.ram);

    /* Prototype */
    ProtoShape base_shape = { clone_shape, 101 };
    ProtoShape *cloned = base_shape.clone(&base_shape);
    printf("  Prototype cloned item ID: %d\n", cloned->id);
    free(cloned);

    /* Adapter */
    TargetInterface adapter_t = { adapter_request };
    adapter_t.request();

    /* Bridge */
    RemoteControl rc = { &tv_impl, remote_toggle_power };
    rc.toggle_power(&rc);

    /* Composite */
    GraphicComponent leaf1 = { leaf_draw, {NULL}, 0 };
    GraphicComponent leaf2 = { leaf_draw, {NULL}, 0 };
    GraphicComponent comp = { composite_draw, {&leaf1, &leaf2}, 2 };
    comp.draw(&comp);

    /* Decorator */
    Coffee simple_c = { simple_coffee_cost };
    MilkDecorator milk_d = { { milk_coffee_cost }, &simple_c };
    printf("  Coffee cost: Simple=$%.2f, Decorated with Milk=$%.2f\n", simple_c.cost(), milk_d.base.cost());

    /* Facade */
    SystemFacade fac = { {facade_sub_a_init}, {facade_sub_b_start}, facade_run };
    fac.run();

    /* Flyweight */
    CharacterFlyweight f_char = { 'A' };
    flyweight_print(&f_char, 12);

    /* Proxy */
    TargetInterface proxy_subject = { proxy_request };
    proxy_subject.request();

    /* Chain of Responsibility */
    RequestHandler h2 = { NULL, concrete_handler_handle };
    RequestHandler h1 = { &h2, concrete_handler_handle };
    h1.handle(&h1, 3);
    h1.handle(&h1, 7);

    /* Command */
    CommandObj cmd = { light_on_execute };
    cmd.execute();

    /* Interpreter */
    Expression expr = { int_interpret, 15 };
    printf("  Interpreter evaluated value: %d\n", expr.interpret(&expr));

    /* Iterator */
    int elements[] = {10, 20, 30};
    VectorIterator vec_iter = { elements, 3, 0, iter_has_next, iter_next };
    printf("  Iterator outputs: ");
    while (vec_iter.has_next(&vec_iter)) {
        printf("%d ", vec_iter.next(&vec_iter));
    }
    printf("\n");

    /* Mediator */
    Participant part1 = { "User1", participant_receive };
    Participant part2 = { "User2", participant_receive };
    ChatMediator med = { &part1, &part2, chat_mediator_send };
    med.send(&med, "Hello World from User1", &part1);

    /* Memento */
    int current_state = 100;
    StateMemento saved_m = originator_save(current_state);
    current_state = 200;
    printf("  State changed to: %d. Restoring...\n", current_state);
    originator_restore(&current_state, saved_m);
    printf("  State restored to: %d\n", current_state);

    /* Observer */
    Observer obs = { obs_update };
    obs.update(&obs, 42);

    /* State */
    state_connected();
    state_disconnected();

    /* Strategy */
    int sort_arr[] = {9, 2, 4, 1};
    SortStrategy strat = { bubble_sort_strategy };
    strat.sort(sort_arr, 4);
    printf("  Strategy sort result: %d %d %d %d\n", sort_arr[0], sort_arr[1], sort_arr[2], sort_arr[3]);

    /* Template Method */
    GameAlgorithm game = { facade_run, facade_run, facade_run, game_play };
    game.play(&game);

    /* Visitor */
    ElementVisitor visitor = { concrete_visitor_visit };
    VisitorElement elem = { 999, element_accept };
    elem.accept(&elem, &visitor);
}
{c_quote})
""".replace("{c_quote}", c_quote)

# Read current build_cs_ds_encyclopedia_c.py
with open("build_cs_ds_encyclopedia_c.py", "r", encoding="utf-8") as f:
    builder_content = f.read()

# Locate the line "''')" of the last section
last_quote_index = builder_content.rfind("''')")
if last_quote_index == -1:
    print("Could not find the last ''') in build_cs_ds_encyclopedia_c.py")
else:
    # Append the chunk_content right after the last quote
    builder_content = builder_content[:last_quote_index + 4] + "\n" + chunk_content
    with open("build_cs_ds_encyclopedia_c.py", "w", encoding="utf-8") as f:
        f.write(builder_content)
    print("Chunk 2 appended successfully!")
