"use strict";
var __extends = (this && this.__extends) || function (d, b) {
    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
    function __() { this.constructor = d; }
    d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
};
var stream_1 = require("stream");
var CountStream = (function (_super) {
    __extends(CountStream, _super);
    function CountStream(matchText, options) {
        var _this = _super.call(this, options) || this;
        _this.count = 0;
        _this.matcher = new RegExp(matchText, 'ig');
        return _this;
    }
    CountStream.prototype._write = function (chunk, encoding, cb) {
        var matches = chunk.toString().match(this.matcher);
        if (matches) {
            this.count += matches.length;
        }
        cb();
    };
    CountStream.prototype.end = function () {
        this.emit('total', this.count);
    };
    return CountStream;
}(stream_1.Writable));
module.exports = CountStream;
