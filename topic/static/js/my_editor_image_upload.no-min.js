
/*
    Markdown editor image upload, should be loaded before $.editor()
    requires: util.js
 */

(function($) {
  var EditorImageUpload,
    bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  EditorImageUpload = (function() {
    EditorImageUpload.prototype.defaults = {
      csrfToken: "csrf_token",
      target: "target url",
      placeholderText: "uploading {image_name}"
    };

    function EditorImageUpload(el, options) {
      this.openFileDialog = bind(this.openFileDialog, this);
      this.textReplace = bind(this.textReplace, this);
      this.addStatusError = bind(this.addStatusError, this);
      this.addError = bind(this.addError, this);
      this.addImage = bind(this.addImage, this);
      this.buildFormData = bind(this.buildFormData, this);
      this.addPlaceholder = bind(this.addPlaceholder, this);
      this.sendFile = bind(this.sendFile, this);
      this.el = $(el);
      this.options = $.extend({}, this.defaults, options);
      this.inputFile = $('<input/>', {
        type: "file",
        accept: "image/*",
        multiple:"multiple"
      });
      this.setUp();
    }

    EditorImageUpload.prototype.setUp = function() {
      var $boxImage;
      if (window.FormData == null) {
        return;
      }
      this.inputFile.on('change', this.sendFile);
      $boxImage = $(".js-box-image");
      $boxImage.on('click', this.openFileDialog);
      return $boxImage.on('click', this.stopClick);
    };

    EditorImageUpload.prototype.sendFile = function() {
      var file, formData, placeholder, post;
      file = this.inputFile.get(0).files[0];
      placeholder = this.addPlaceholder(file);
      formData = this.buildFormData(file);
      post = $.ajax({
        url: this.options.target,
        data: formData,
        processData: false,
        contentType: false,
        type: 'POST'
      });
      post.done((function(_this) {
        return function(data) {
          if ("url" in data) {
            return _this.addImage(data, file, placeholder);
          } else {
            return _this.addError(data, placeholder);
          }
        };
      })(this));
      post.fail((function(_this) {
        return function(jqxhr, textStatus, error) {
          return _this.addStatusError(textStatus, error, placeholder);
        };
      })(this));
    };

    EditorImageUpload.prototype.addPlaceholder = function(file) {
      var placeholder;
      placeholder = $.format("![" + this.options.placeholderText + "]()", {
        image_name: file.name
      });
      this.el.val(this.el.val() + placeholder);
      return placeholder;
    };

    EditorImageUpload.prototype.buildFormData = function(file) {
      var formData;
      formData = new FormData();
      formData.append('csrfmiddlewaretoken', this.options.csrfToken);
      formData.append('image', file);
      return formData;
    };

    EditorImageUpload.prototype.addImage = function(data, file, placeholder) {
      //var imageTag;
      //imageTag = $.format("![{name}]({url})", {
      //  name: file.name,
      //  url: data.url
      //});
      //return this.textReplace(placeholder, imageTag);
      var $el = $.format('<li class="item"><img src="{src}" cmid="{cmid}" style="width:100%;height:100%;"></li>',{
        src:data.url,
        cmid:data.cmid
      });
      this.el.prepend($el);
    };

    EditorImageUpload.prototype.addError = function(data, placeholder) {
      var error;
      error = JSON.stringify(data);
      return this.textReplace(placeholder, "![" + error + "]()");
    };

    EditorImageUpload.prototype.addStatusError = function(textStatus, error, placeholder) {
      var errorTag;
      errorTag = $.format("![error: {code} {error}]()", {
        code: textStatus,
        error: error
      });
      return this.textReplace(placeholder, errorTag);
    };

    EditorImageUpload.prototype.textReplace = function(find, replace) {
      this.el.val(this.el.val().replace(find, replace));
    };

    EditorImageUpload.prototype.openFileDialog = function() {
      this.inputFile.trigger('click');
    };

    EditorImageUpload.prototype.stopClick = function(e) {
      e.preventDefault();
      e.stopPropagation();
      e.stopImmediatePropagation();
    };

    return EditorImageUpload;

  })();

  $.fn.extend({
    editor_image_upload: function(options) {
      return this.each(function() {
        if (!$(this).data('plugin_editor_image_upload')) {
          return $(this).data('plugin_editor_image_upload', new EditorImageUpload(this, options));
        }
      });
    }
  });

  $.fn.editor_image_upload.EditorImageUpload = EditorImageUpload;

}).call(this,jQuery);