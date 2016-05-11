function getViewSize() {
    return {
        "h": window['innerHeight'] || document.documentElement.clientHeight
    }
}
 
function getFullSize() {
 
    Math.max(document.documentElement.scrollLeft, document.body.scrollLeft);
    var h = Math.max(document.documentElement.clientHeight, document.body.clientHeight) +
 
    Math.max(document.documentElement.scrollTop, document.body.scrollTop);
    h = Math.max(document.documentElement.scrollHeight, h);
    return {
        "h": h
    };
}
 
function setContainerSize() {
    size = getViewSize();
    console.log(size);
    document.getElementById("Heightauto").style.height = size["h"] - 40 + "px";
}
 
setContainerSize();
window.onresize = setContainerSize;