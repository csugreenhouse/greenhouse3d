import cv2
import numpy as np
import apriltag
import matplotlib.pyplot as plt
import warnings
import matplotlib.patches as patches
from matplotlib.lines import Line2D

color_pallet = ['cyan', 'yellow', 'magenta', 'orange', 'pink', 'lime', 'aqua']

import utils.cameracapture as cameracapture

def scan_raw_tags(image):
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    options = apriltag.DetectorOptions(families="tag25h9")
    detector = apriltag.Detector(options)
    results = detector.detect(gray)
    return results

def sort_corners(corners):
    """
    Sort corners in the order: top_left, top_right, bottom_right, bottom_left
    """
    corners = np.array(corners)
    s = corners.sum(axis=1)
    diff = np.diff(corners, axis=1)

    top_left = corners[np.argmin(s)]
    bottom_right = corners[np.argmax(s)]
    top_right = corners[np.argmin(diff)]
    bottom_left = corners[np.argmax(diff)]

    return [top_left, top_right, bottom_right, bottom_left]

def scan_apriltags(image):
    results = scan_raw_tags(image)

    DECISION_MARGIN = 40.0
    valid_tags = []
    

    for tag in results:
        corners_sorted = sort_corners(tag.corners)
        #print(f"TAG ID {tag.tag_id} with decision margin {tag.decision_margin}")
        if (tag.decision_margin>DECISION_MARGIN):
            # color_bounds, scale_units_m, bias_units_m = parse_qr_data(str(tag.tag_id))
            # Expected order is typically TL, TR, BR, BL (matches your current indexing)
            tag = {
                "data": int(tag.tag_id),
                "tag_type": "apriltag",
                "center": tuple(np.asarray(tag.center, dtype=np.float32)),
                "corners": {
                    # RELATIVE TO THE IMAGE, Y INCREASES DOWNWARDS, THUS SWITCH THE ORDER
                    "top_left": tuple(corners_sorted[0]),
                    "top_right": tuple(corners_sorted[1]),
                    "bottom_right": tuple(corners_sorted[2]),
                    "bottom_left": tuple(corners_sorted[3]),
                },
            }
            valid_tags.append(tag)

    if len(valid_tags) == 0:
        if len(results) != 0:
            raise ValueError("No valid april tag has been detected, but a non valid one has been found")
        else:
            raise ValueError("No april tags at all have been found")
    return valid_tags

def plot_reference_tag(image,out_path, reference_tag):
    graph_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    W,H = graph_rgb.shape[1], graph_rgb.shape[0]
    fig, ax = plt.subplots()
    ax.imshow(graph_rgb)
    ax.axis('on')

    add_tag(ax,reference_tag)
    views = reference_tag["views"]

    for i, view in enumerate(views):
        add_view(ax,W,H,view,facecolor=color_pallet[i])
 
    ax.set_title("REFERENCE TAG")

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),ncol=2)
    plt.savefig(str(out_path), bbox_inches="tight")
    plt.close(fig)