var Finance = function () { };

Finance.prototype.PV = function (rate, nper, pmt, fv, type) {
  type = typeof type === "undefined" ? 0 : type;
  fv = typeof fv === "undefined" ? 0 : fv;
  if (rate === 0) {
    return -pmt * nper - fv;
  } else {
    var tempVar = type !== 0 ? 1 + rate : 1;
    var tempVar2 = 1 + rate;
    var tempVar3 = Math.pow(tempVar2, nper);
    return -(fv + pmt * tempVar * ((tempVar3 - 1) / rate)) / tempVar3;
  }
};

Finance.prototype.FV = function (rate, nper, pmt, pv, type) {
  type = typeof type === "undefined" ? 0 : type;
  if (rate === 0) {
    return -pv - pmt * nper;
  } else {
    var tempVar = type !== 0 ? 1 + rate : 1;
    var tempVar2 = 1 + rate;
    var tempVar3 = Math.pow(tempVar2, nper);
    return -pv * tempVar3 - (pmt / rate) * tempVar * (tempVar3 - 1);
  }
};

Finance.prototype.EVALNPV = function (rate, values, npvType, lowerBound, upperBound) {
  var tempVar = 1;
  var tempTotal = 0;
  var i = lowerBound;
  while (i <= upperBound) {
    var tempVar2 = values[i];
    tempVar = tempVar + tempVar * rate;
    if (!(npvType > 0 && tempVar2 > 0) || !(npvType < 0 && tempVar2 < 0)) {
      tempTotal = tempTotal + tempVar2 / tempVar;
    }
    i++
  }
  return tempTotal
};

Finance.prototype.NPV = function (rate) {
  var values = Array.prototype.slice.call(arguments).slice(1);
  var lowerBound = 0;
  var upperBound = values.length - 1;
  var tempVar = upperBound - lowerBound + 1;
  if (tempVar < 1) {
    return "Error - Invalid Values"
  }
  if (rate === -1) {
    return "Error - Invalid Rate"
  }
  return this.EVALNPV(rate, values, 0, lowerBound, upperBound);
};

Finance.prototype.InternalPV = function (values, guess) {
  guess = typeof guess === "undefined" ? 0.1 : guess;
  var lowerBound = 0;
  var upperBound = values.length - 1;
  var tempTotal = 0
  var divRate = 1 + guess;
  while (lowerBound <= upperBound && values[lowerBound] === 0) {
    lowerBound++;
  }
  var i = upperBound;
  var step = -1
  while (i >= lowerBound) {
    tempTotal = tempTotal / divRate;
    tempTotal = tempTotal + values[i];
    i = i + step;
  }
  return tempTotal;
}

Finance.prototype.IRR = function (values, guess) {
  guess = typeof guess === "undefined" ? 0.1 : guess;
  var epslMax = 0.0000001;
  var step = 0.00001;
  var iterMax = 39;
  //Check for valid inputs
  if (guess <= -1) {
    return "Error - invalid guess";
  }
  if (values.length < 1) {
    return null;
  }
  //Scale up the Epsilon Max based on cash flow values
  var tempVar = values[0] > 0 ? values[0] : values[0] * -1;
  var i = 0;
  while (i < values.length) {
    if (Math.abs(values[i]) > tempVar) {
      tempVar = Math.abs(values[i]);
    }
    i++;
  }
  tempNpvEpsl = tempVar * epslMax * 0.01
  tempRate0 = guess;
  tempNpv0 = this.InternalPV(values, tempRate0);
  var tempRate1 = tempNpv0 > 0 ? tempRate0 + step : tempRate0 - step;
  if (tempRate1 <= -1) {
    return "Error - invalid values";
  }
  var tempNpv1 = this.InternalPV(values, tempRate1);
  var i = 0;
  while (i <= iterMax) {
    if (tempNpv1 === tempNpv0) {
      tempRate0 = tempRate1 > tempRate0 ? tempRate0 - step : tempRate0 + step;

      tempNpv0 = this.InternalPV(values, tempRate0);

      if (tempNpv1 === tempNpv0) {
        return "Error - invalid values";
      }
    }
    tempRate0 = tempRate1 - (tempRate1 - tempRate0) * tempNpv1 / (tempNpv1 - tempNpv0);
    //Secant method
    if (tempRate0 <= -1) {
      tempRate0 = (tempRate1 - 1) * 0.5;
    }
    //Give the algorithm a second chance...
    tempNpv0 = this.InternalPV(values, tempRate0);
    tempVar = tempRate0 > tempRate1 ? tempRate0 - tempRate1 : tempRate1 - tempRate0;
    var tempVar2 = tempNpv0 > 0 ? tempNpv0 : tempNpv0 * -1;
    //Test for npv = 0 and rate convergence
    if (tempVar2 < tempNpvEpsl && tempVar < epslMax) {
      return tempRate0;
    }
    //Transfer values and try again...
    tempVar = tempNpv0;
    tempNpv0 = tempNpv1;
    tempNpv1 = tempVar;
    tempVar = tempRate0;
    tempRate0 = tempRate1;
    tempRate1 = tempVar;
    i++;
  }
  return "Error - iterMax exceeded"
};

var finance = new Finance();
