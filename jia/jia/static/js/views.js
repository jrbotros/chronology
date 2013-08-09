if (typeof(Jia) === "undefined") {
  var Jia = {};
}

$(function() {
  Jia.VisView = Backbone.View.extend({
    tagName : "li",

    className : "view",

    id : function() {
        return this.model.get("hash");
    },

    initialize : function() {
      this.listenTo(this.model, "change", this.render);
    },

    // Templates defined in templates/index.html
    viewTypeToTemplate : {
      "plot": _.template($("#plot-vis").html()),
      "table": _.template($("#table-vis").html()),
    },

    render : function() {
      var type = this.model.get("type");
      if (type == "plot") {
       this.render_plot();
      } else if (type == "table") {
        this.render_table();
      } else {
        console.log("VisView: Unknown model type ["+type+"]");
        return;
      }

      this.$el.find(".remove-vis").click((function(view) {
        return function() {
          var views = Backbone.history.getHash();
          views = (views && views.split("/")) || [];
          var new_views = _.without(views, view.model.get("hash"));
          Jia.router.navigate(new_views.join("/"));

          view.$el.remove();
          Jia.main.remove(view);
        }
      })(this));

      return this;
    },

    render_plot : function() {
      var template = this.viewTypeToTemplate["plot"];
      this.$el.html(template(this.model.attributes));
      makeGraph(this.model.get("data"), this.$el);
    },

    render_table : function() {
      var template = this.viewTypeToTemplate["table"];
      this.$el.html(template(this.model.attributes));
      makeTable(this.model.get("data"), this.$el);
    },
  });


  Jia.MainView = Backbone.View.extend({
    el: $("#visualizations"),

    initialize: function() {
      this.collection = this.options.collection;
      this.listenTo(this.collection, "add", this.addOne);
      this.listenTo(this.collection, "reset", this.addAll);
      this.listenTo(this.collection, "all", this.render);
      this.render();
    },

    addOne: function(vis) {
      var view = new Jia.VisView({model: vis});
      this.$el.append(view.render().el);
    },

    addAll: function() {
      this.collection.each(this.addOne, this);
    },

    remove: function(view) {
      this.collection.remove(view);
    },
  });
});