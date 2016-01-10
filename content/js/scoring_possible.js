var bossylobsterBlog = bossylobsterBlog || {};
bossylobsterBlog.FBScore = bossylobsterBlog.FBScore || {};

bossylobsterBlog.FBScore.SCORES = [2, 3, 6, 7, 8];
bossylobsterBlog.FBScore.SCORE_MAPPING = {
    2: 'Safety',
    3: 'Field Goal',
    6: 'TD with missed PAT',
    7: 'TD',
    8: 'TD with 2P conversion',
};


bossylobsterBlog.FBScore.getCombos = function(total, vals) {
    if (vals.length === 0) {
        if (total === 0) {
            return [[]];
        } else {
            return [];
        }
    }

    var result = [];
    var currVal = vals[0];
    var remainingVals = vals.slice(1);

    var currMultiple = 0;
    var currMultiplier = 0;
    var subResult, i, subVal;
    while (currMultiple <= total) {
        subResult = bossylobsterBlog.FBScore.getCombos(total - currMultiple, remainingVals);
        for (i = 0; i < subResult.length; i++) {
            subVal = subResult[i];
            result.push([currMultiplier].concat(subVal));
        }
        currMultiple += currVal;
        currMultiplier += 1;
    }

    return result;
};


bossylobsterBlog.FBScore.getScoringPlays = function(score) {
    var result = [];
    var allCombos = bossylobsterBlog.FBScore.getCombos(score, bossylobsterBlog.FBScore.SCORES);
    var i, currInfo, j, numScores, scoringPlay, scoreDescription;
    for (i = 0; i < allCombos.length; i++) {
        currInfo = [];
        for (j = 0; j < bossylobsterBlog.FBScore.SCORES.length; j++) {
            numScores = allCombos[i][j];
            scoringPlay = bossylobsterBlog.FBScore.SCORES[j];
            scoreDescription = bossylobsterBlog.FBScore.SCORE_MAPPING[scoringPlay];
            if (numScores !== 0) {
                currInfo.push(numScores.toString() + ' x ' + scoreDescription);
            }
        }
        result.push(currInfo.join(', '));
    }
    return result;
};

bossylobsterBlog.FBScore.updatePage = function() {
    var numPoints = document.getElementById('num-points');
    numPoints = parseInt(numPoints.value);
    if (!isFinite(numPoints)) {
        return;
    }
    if (numPoints < 1) {
        return;
    }

    var scoresOL = document.getElementById('scores-list');
    var scoringPlays = bossylobsterBlog.FBScore.getScoringPlays(numPoints);

    // Remove existing list elements.
    while (scoresOL.firstChild) {
        scoresOL.removeChild(scoresOL.firstChild);
    }

    // Add new list elements.
    var i, liNode;
    for (i = 0; i < scoringPlays.length; i++) {
        liNode = document.createElement('li');
        liNode.innerText = scoringPlays[i];
        scoresOL.appendChild(liNode);
    }
};
