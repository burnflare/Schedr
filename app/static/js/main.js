requirejs.config({
  baseUrl: "/js/vendor",
  paths: {
      "jquery": "//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min",
      "bootstrap" : "bootstrap.min",
    },
    shim: {
      "can.custom": {
        deps: ["jquery"],
        exports: 'can'
      },
      "bootstrap": ["jquery"]
   }
 });
 
 requirejs(["../router"]);