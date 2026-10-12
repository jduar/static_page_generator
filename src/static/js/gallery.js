let preferMaxHeight = 450;
const padding = 10;

window.addEventListener("load", buildGallery);
if (!isPhone()) {
  window.addEventListener("resize", buildGallery);
}

function buildGallery() {
  setPreferredMaxHeight();

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
      if (!isPhone()) {
        const proposedWidth = calculateImgWidth(image);

        if (rowWidth + proposedWidth + 2 * padding <= maxWidth) {
          rowWidth += proposedWidth + 2 * padding;
          positionInRow++;
        } else if (
          rowWidth + proposedWidth + 2 * padding > maxWidth &&
          positionInRow === 0
        ) {
          element.style.height = calculateImgHeight(image, maxWidth);
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
    for (let position = 0; position < positionInRow; position++) {
      let divIndex = images.length - position - 1;
      setDivSize(
        images[divIndex],
        preferMaxHeight,
        calculateImgWidth(getImageWithin(images[divIndex]))
      );
    }
  }
}

function getImageWithin(div) {
  return div.querySelector(".gallery-image");
}

function calculateImgWidth(image, height = preferMaxHeight) {
  var ratio = height / image.getAttribute("height");
  return image.getAttribute("width") * ratio;
}

function calculateImgHeight(image, width) {
  var ratio = width / image.getAttribute("width");
  return image.getAttribute("height") * ratio;
}

function setDivSize(div, height, width) {
  div.style.height = height + "px";
  div.style.width = width + "px";
}

function adjustImagesToFit(divs, maxWidth) {
  var ratios = [];
  for (let i = 0; i < divs.length; i++) {
    var image = getImageWithin(divs[i]);
    ratios.push(image.getAttribute("width") / image.getAttribute("height"));
  }
  const realRatio = maxWidth / ratios.reduce((partialSum, a) => partialSum + a, 0);
  for (let i = 0; i < divs.length; i++) {
    setDivSize(
      divs[i],
      calculateImgHeight(getImageWithin(divs[i]), realRatio * ratios[i]),
      realRatio * ratios[i] - 2 * padding
    );
  }
}

function setPreferredMaxHeight() {
  const windowWidth = window.innerWidth;

  if (windowWidth >= 1920 && windowWidth < 2560) {
    preferMaxHeight = 525;
  } else if (windowWidth >= 2560) {
    preferMaxHeight = 650;
  } else {
    preferMaxHeight = 450;
  }
}

function isPhone() {
  return window.innerWidth < 600;
}
