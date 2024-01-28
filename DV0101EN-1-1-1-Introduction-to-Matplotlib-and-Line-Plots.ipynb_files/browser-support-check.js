/* String.endsWith polyfill */
if (!String.prototype.endsWith) {
  String.prototype.endsWith = function(searchString, position) {
      var subjectString = this.toString();
      if (typeof position !== 'number' || !isFinite(position)
          || Math.floor(position) !== position || position > subjectString.length) {
        position = subjectString.length;
      }
      position -= searchString.length;
      var lastIndex = subjectString.indexOf(searchString, position);
      return lastIndex !== -1 && lastIndex === position;
  };
}

/* Array.find polyfill */
// https://tc39.github.io/ecma262/#sec-array.prototype.find
if (!Array.prototype.find) {
  Object.defineProperty(Array.prototype, 'find', {
    value: function(predicate) {
     // 1. Let O be ? ToObject(this value).
      if (this == null) {
        throw new TypeError('"this" is null or not defined');
      }

      var o = Object(this);

      // 2. Let len be ? ToLength(? Get(O, "length")).
      var len = o.length >>> 0;

      // 3. If IsCallable(predicate) is false, throw a TypeError exception.
      if (typeof predicate !== 'function') {
        throw new TypeError('predicate must be a function');
      }

      // 4. If thisArg was supplied, let T be thisArg; else let T be undefined.
      var thisArg = arguments[1];

      // 5. Let k be 0.
      var k = 0;

      // 6. Repeat, while k < len
      while (k < len) {
        // a. Let Pk be ! ToString(k).
        // b. Let kValue be ? Get(O, Pk).
        // c. Let testResult be ToBoolean(? Call(predicate, T, « kValue, k, O »)).
        // d. If testResult is true, return kValue.
        var kValue = o[k];
        if (predicate.call(thisArg, kValue, k, o)) {
          return kValue;
        }
        // e. Increase k by 1.
        k++;
      }

      // 7. Return undefined.
      return undefined;
    },
    configurable: true,
    writable: true
  });
}

function redirectUnsupportedBrowser() {

    if (window.location.href.endsWith('unsupported')) {
        // already on the unsupported browser page
        return;
    }
    console.log('checking for browser compatibility');

    var browser = bowser.getParser(window.navigator.userAgent);

    // browsers that are known to be incompatible with SN Labs:
    var isUnsupportedBrowser = browser.satisfies({
        "Internet Explorer": ">0",
        "Edge": "<15",
        // "Firefox": "<5",
        "windows": {
            "Firefox": "<52",
        },
        "macos": {
            "Firefox": "<52",
        },
        "mobile": {
            "Safari": ">0"
        }
    });

    // browsers that don't support labs being rendered
    // in an iframe that's not on the labs base domain:
    var hasStrictIframeSecurity = browser.satisfies({
        "Safari": ">0"
    });

    function inIframe() {
        return window.self === window.top;
    };

    function baseDomainDoesNotMatch() {
        try {
        var labsBaseDomain =  window.location.hostname.split('.').slice(1).join('.');
        var outerDomain = window.top.location.hostname;
        return !outerDomain.endsWith(labsBaseDomain);
        } catch (err) {
        // if we can't even check if the domains match,
        // we're probably not on the same base domain
        if (err.toString().includes("SecurityError: Blocked")) {
            return true;
        };
        if (Raven) {
            Raven.capture(err);
        };
        return false; // don't return true unless we're sure
        };
    };

    if (
        isUnsupportedBrowser ||
        hasStrictIframeSecurity && inIframe() && baseDomainDoesNotMatch()
    ) {
        // redirect to unsupported page
        window.location.href = '/unsupported';
    };
}

redirectUnsupportedBrowser();
