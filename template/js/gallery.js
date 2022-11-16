window.onload = buildGallery;
window.onresize = buildGallery;

var preferMaxHeight = 450;

function buildGallery() {
  var gallery = document.getElementById("gallery");
  var images = document.getElementsByClassName("image-outer");

  var maxWidth = gallery.offsetWidth - 1;

  let row = 0;
  let rowWidth = 0;

  let positionInRow = 0;

  for (let img_index = 0; img_index < images.length; img_index++) {
    proposedWidth = calculateWidth(images[img_index]);

    if (rowWidth + proposedWidth <= maxWidth) {
      rowWidth += proposedWidth;
      positionInRow++;
      console.log("menor", proposedWidth);
    } else if (rowWidth + proposedWidth > maxWidth && positionInRow === 0) {
      images[img_index].height = calculateHeight(images[img_index], maxWidth);
      row++;
    } else if (rowWidth + proposedWidth > maxWidth && positionInRow > 0) {
      var imagesToAdjust = [];
      for (let position = 0; position <= positionInRow; position++) {
        imagesToAdjust.push(images[img_index - (positionInRow - position)]);
      }
      console.log("row", row);
      adjustImagesToFit(imagesToAdjust, maxWidth);

      row++;
      rowWidth = 0;
      positionInRow = 0;
    } else {
      console.log("coco");
    }
  }
};

function getImageWithin(div) {
  return div.getElementsByClassName("image-temp")[0];
}

function calculateWidth(div, height = preferMaxHeight) {
  var ratio = height / getImageWithin(div).naturalHeight;
  return getImageWithin(div).naturalWidth * ratio;
}

function calculateHeight(div, width) {
  var ratio = width / getImageWithin(div).naturalWidth;
  return getImageWithin(div).naturalHeight * ratio;
}

function setSize(div, height, width) {
  div.style.height = height + "px";
  div.style.width = width + "px";
}

function adjustImagesToFit(divs, maxWidth) {
  var ratios = [];
  for (let i = 0; i < divs.length; i++) {
    var image = getImageWithin(divs[i]);
    // ratios.push(preferMaxHeight / image.naturalHeight);
    ratios.push(image.naturalWidth / image.naturalHeight);
  }
  const realRatio =
    maxWidth / ratios.reduce((partialSum, a) => partialSum + a, 0);
  console.log("maxWidth", maxWidth);
  console.log(ratios.reduce((partialSum, a) => partialSum + a, 0));
  console.log("realRatio", realRatio);
  for (let i = 0; i < divs.length; i++) {
    console.log(
      "ratio",
      ratios[i],
      "height",
      calculateHeight(divs[i], realRatio * ratios[i]),
      "width",
      realRatio * ratios[i]
    );
    setSize(
      divs[i],
      calculateHeight(divs[i], realRatio * ratios[i]),
      realRatio * ratios[i]
    );
  }
}