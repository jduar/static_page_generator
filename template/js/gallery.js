window.onload = buildGallery;
window.onresize = buildGallery;

var preferMaxHeight = 450;
var padding = 5;

function buildGallery() {
  var windowWidth = window.innerWidth;
  if (windowWidth >= 865) {
    // We only need CSS on small screens.
    var gallery = document.getElementById("gallery");

    if (gallery) {
      var images = document.getElementsByClassName("image-outer");

      var maxWidth = gallery.offsetWidth - 1;

      let row = 0;
      let rowWidth = 0;

      let positionInRow = 0;

      for (let img_index = 0; img_index < images.length; img_index++) {
        proposedWidth = calculateWidth(images[img_index]);

        if (rowWidth + proposedWidth + 2 * padding <= maxWidth) {
          rowWidth += proposedWidth;
          positionInRow++;
        } else if (
          rowWidth + proposedWidth + 2 * padding > maxWidth &&
          positionInRow === 0
        ) {
          images[img_index].height = calculateHeight(images[img_index], maxWidth);
          row++;
        } else if (
          rowWidth + proposedWidth + 2 * padding > maxWidth &&
          positionInRow > 0
        ) {
          var imagesToAdjust = [];
          for (let position = 0; position <= positionInRow; position++) {
            imagesToAdjust.push(images[img_index - (positionInRow - position)]);
          }
          adjustImagesToFit(imagesToAdjust, maxWidth);

          row++;
          rowWidth = 0;
          positionInRow = 0;
        }
        loadImage(images[img_index]);
      }
    }
  }
}

function getImageWithin(div) {
  return div.getElementsByClassName("gallery-image")[0];
}

function calculateWidth(div, height = preferMaxHeight) {
  let image = getImageWithin(div);
  var ratio = height / image.naturalHeight;
  return image.naturalWidth * ratio;
}

function calculateHeight(div, width) {
  let image = getImageWithin(div);
  var ratio = width / image.naturalWidth;
  return image.naturalHeight * ratio;
}

function setSize(div, height, width) {
  div.style.height = height + "px";
  div.style.width = width + "px";
}

function adjustImagesToFit(divs, maxWidth) {
  var ratios = [];
  for (let i = 0; i < divs.length; i++) {
    var image = getImageWithin(divs[i]);
    ratios.push(image.naturalWidth / image.naturalHeight);
  }
  const realRatio =
    maxWidth / ratios.reduce((partialSum, a) => partialSum + a, 0);
  for (let i = 0; i < divs.length; i++) {
    setSize(
      divs[i],
      calculateHeight(divs[i], realRatio * ratios[i]),
      realRatio * ratios[i] - 2 * padding
    );
  }
}

function setPreferredMaxHeight() {
  if (windowWidth >= 865 && windowWidth < 1080) {
    preferMaxHeight = 180;
  } else if (windowWidth >= 1080 && windowWidth < 1920) {
    preferMaxHeight = 290;
  } else if (windowWidth >= 1080 && windowWidth < 2560) {
    preferMaxHeight = 350;
  } else if (windowWidth >= 2560) {
    preferMaxHeight = 450;
  }
}

function loadImage(image_div) {
  let image = getImageWithin(image_div);
  image.src = image.getAttribute("data-src");
}