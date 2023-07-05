var preferMaxHeight = 450;
const padding = 10;

window.addEventListener("load", buildGallery);
if (desktop(window.innerWidth) === true) {
  window.addEventListener("resize", buildGallery);
}

function buildGallery() {
  const gallery = document.getElementById("gallery");

  if (gallery) {
    const images = gallery.querySelectorAll(".image-outer");
    const maxWidth = gallery.offsetWidth - 1;

    let rowWidth = 0;
    let positionInRow = 0;

    images.forEach((element, index) => {
      const image = getImageWithin(element);
      image.classList.remove("jsonly");

      // If we're on mobile, let the CSS do its thing.
      if (desktop(window.innerWidth) === true) {
        const proposedWidth = calculateWidth(image);

        if (rowWidth + proposedWidth + 2 * padding <= maxWidth) {
          rowWidth += proposedWidth + 2 * padding;
          positionInRow++;
        } else if (
          rowWidth + proposedWidth + 2 * padding > maxWidth &&
          positionInRow === 0
        ) {
          element.style.height = calculateHeight(image, maxWidth);
        } else if (
          rowWidth + proposedWidth + 2 * padding > maxWidth &&
          positionInRow > 0
        ) {
          let imagesToAdjust = [];
          for (let position = 0; position <= positionInRow; position++) {
            imagesToAdjust.push(images[index - (positionInRow - position)]);
          }
          adjustImagesToFit(imagesToAdjust, maxWidth);
          rowWidth = 0;
          positionInRow = 0;
        }
      }
    });

    // Adjust pictures on the remaining row
    let imagesToAdjust = [];
    for (let position = 0; position < positionInRow; position++) {
      imagesToAdjust.push(images[images.length - position - 1]);
    }
    adjustImagesToFit(imagesToAdjust, maxWidth);
  }
}

function getImageWithin(div) {
  return div.querySelector(".gallery-image");
}

function calculateWidth(image, height = preferMaxHeight) {
  var ratio = height / image.getAttribute("height");
  return image.getAttribute("width") * ratio;
}

function calculateHeight(image, width) {
  var ratio = width / image.getAttribute("width");
  return image.getAttribute("height") * ratio;
}

function setSize(div, height, width) {
  div.style.height = height + "px";
  div.style.width = width + "px";
}

function adjustImagesToFit(divs, maxWidth) {
  var ratios = [];
  for (let i = 0; i < divs.length; i++) {
    var image = getImageWithin(divs[i]);
    ratios.push(image.getAttribute("width") / image.getAttribute("height"));
  }
  const realRatio =
    maxWidth / ratios.reduce((partialSum, a) => partialSum + a, 0);
  for (let i = 0; i < divs.length; i++) {
    setSize(
      divs[i],
      calculateHeight(getImageWithin(divs[i]), realRatio * ratios[i]),
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

function desktop(width) {
  return width >= 865 ? true : false;
}
