function loadCanvas(id) {
        var canvas = document.createElement('canvas');
        div = document.getElementById(id); 
        canvas.id     = "CursorLayer";
        canvas.width  = 640;
        canvas.height = 480;
        canvas.style.zIndex   = 8;
        canvas.style.position = "absolute";
        canvas.style.border   = "1px solid";
        div.appendChild(canvas)
        return canvas;
}
// https://stackoverflow.com/questions/11332608/understanding-html-5-canvas-scale-and-translate-order
function drawgrid(canvas) {
    var width = canvas.width;
    var height = canvas.height;
    ctx = canvas.getContext('2d');
    for (var i = 0; i < width; i += 10) {
        ctx.moveTo(i + 0.5, 0);
        ctx.lineTo(i + 0.5, height)
    }

    for (var i = 0; i < height; i += 10) {
        ctx.moveTo(0, i + 0.5);
        ctx.lineTo(width, i + 0.5)
    }
    ctx.strokeStyle = 'rgba(0, 0, 0, 0.2);'
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(-width * 2, 0);
    ctx.lineTo(width * 2, 0);
    ctx.moveTo(0, -height * 2);
    ctx.lineTo(0, height * 2);
    ctx.lineWidth = 8;
    ctx.strokeStyle = 'red';
    ctx.stroke();
}
function apply_ts(canvas) {
    ctx = canvas.getContext('2d');
    ctx.scale(2,2);
    ctx.translate(100, 100);
    //ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.resetTransform();
}
canvas = loadCanvas('layer1');
apply_ts(canvas);
drawgrid(canvas);
