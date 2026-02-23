
import pytest
import pandas as pd
import numpy as np
from app.services.pipeline_service import _filter_rare_classes

def test_filter_rare_classes_string_target():
    # Setup: 3 classes, one rare (<2)
    df = pd.DataFrame({'f1': [1, 2, 3, 4, 5]})
    target = pd.Series(['A', 'A', 'B', 'B', 'C']) # C is rare (1 count)
    warnings = []

    # Case 1: Drop rare classes = True
    df_res, target_res, stop = _filter_rare_classes(df, target, drop_rare=True, warnings=warnings)

    assert len(target_res) == 4
    assert 'C' not in target_res.values
    assert len(df_res) == 4
    assert len(warnings) == 1
    assert "Dropped classes with <2 samples: C" in warnings[0]
    assert stop is False

    # Case 2: Drop rare classes = False
    with pytest.raises(ValueError, match="Classes with too few members"):
        _filter_rare_classes(df, target, drop_rare=False, warnings=[])

def test_filter_rare_classes_numeric_target():
    # Setup: 3 classes, one rare
    df = pd.DataFrame({'f1': [1, 2, 3, 4, 5]})
    target = pd.Series([0, 0, 1, 1, 2]) # 2 is rare
    warnings = []

    # Case 1: Drop rare classes = True
    df_res, target_res, stop = _filter_rare_classes(df, target, drop_rare=True, warnings=warnings)

    assert len(target_res) == 4
    assert 2 not in target_res.values
    assert len(df_res) == 4
    assert len(warnings) == 1
    # Check that warning message is correct
    assert "Dropped classes with <2 samples" in warnings[0]
    assert "2" in warnings[0]
    assert stop is False

def test_filter_rare_classes_numpy_target():
    # Setup: Target as numpy array (simulating output of LabelEncoder)
    df = pd.DataFrame({'f1': [1, 2, 3, 4, 5]})
    target = np.array([0, 0, 1, 1, 2]) # 2 is rare
    warnings = []

    # Case 1: Drop rare classes = True
    df_res, target_res, stop = _filter_rare_classes(df, target, drop_rare=True, warnings=warnings)

    # target_res might be series or array depending on implementation details of _filter_rare_classes
    # The current implementation returns target[mask], which for numpy array returns numpy array

    assert len(target_res) == 4
    assert 2 not in target_res
    assert len(df_res) == 4
    assert stop is False

def test_filter_rare_classes_all_rare():
    # Setup: All classes are rare
    df = pd.DataFrame({'f1': [1, 2, 3]})
    target = pd.Series(['A', 'B', 'C'])
    warnings = []

    # Case 1: Drop rare classes = True
    # Should result in empty dataset or stop=True if unique classes < 2
    df_res, target_res, stop = _filter_rare_classes(df, target, drop_rare=True, warnings=warnings)

    assert stop is True
    assert "Insufficient classes" in warnings[-1]
