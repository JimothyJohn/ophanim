import os

import pytest

from detection.coco import CocoClassMapper
from detection.onnx_detector import COCO_91_IDS, COCO_91_TO_80

pytestmark = pytest.mark.unit

COCO_YAML = os.path.join(
    os.path.dirname(__file__), "..", "..", "detection", "coco.yaml"
)


@pytest.fixture(scope="module")
def mapper() -> CocoClassMapper:
    return CocoClassMapper(COCO_YAML)


def test_mapper_direct_lookup_no_offset(mapper: CocoClassMapper) -> None:
    # YOLOv8 / coco.yaml class_ids are the contiguous 0-79 index and must map directly.
    detections = [
        {"class_id": 0},
        {"class_id": 16},
        {"class_id": 17},
        {"class_id": 27},
    ]
    result = mapper.map_class_names(detections)
    names = [d["class_name"] for d in result]
    assert names == ["person", "dog", "horse", "tie"]


def test_mapper_unknown_id(mapper: CocoClassMapper) -> None:
    out = mapper.map_class_names([{"class_id": -1}, {}])
    assert [d["class_name"] for d in out] == ["Unknown", "Unknown"]


def test_coco91_mapping_is_complete_and_ordered() -> None:
    # 80 classes, strictly increasing original COCO IDs, contiguous 0-79 targets.
    assert len(COCO_91_IDS) == 80
    assert COCO_91_IDS == sorted(COCO_91_IDS)
    assert set(COCO_91_TO_80.values()) == set(range(80))


@pytest.mark.parametrize(
    "raw_id,expected_name",
    [
        (1, "person"),  # gap-free prefix
        (18, "dog"),  # the reported regression: 18 must not become horse
        (19, "horse"),
        (32, "tie"),  # tie sits after the COCO-91 gaps
        (90, "toothbrush"),
    ],
)
def test_rfdetr_id_resolves_to_correct_name(
    mapper: CocoClassMapper, raw_id: int, expected_name: str
) -> None:
    class_id = COCO_91_TO_80[raw_id]
    out = mapper.map_class_names([{"class_id": class_id}])
    assert out[0]["class_name"] == expected_name
