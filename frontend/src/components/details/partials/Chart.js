import React from "react";
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import {formatMoney} from "../../utils/formatting";
import highchartsMore from 'highcharts/highcharts-more';

highchartsMore(Highcharts);

export const Chart = ({data}) => {

  const xCategories = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
    "" // Extra value to have extra space on the right side of chart
  ];

  const round = (number) => {
    return Math.round(number * 100) / 100
  }

  const toSumArray = (currentArray) => {
    if (!currentArray.length) return []

    let newArray = [];
    let prevVal = 0;


    for (let value of currentArray) {
      let newVal = value + prevVal;
      newArray.push(round(newVal));
      prevVal = newVal;
    }
    return newArray;
  };


  /* This function properly formats data for arearange series
     Format: [[key, lower, upper]]

     The whole range from January to December is calculated.
     The data from past months will be hidden in chart series options
  */
  const rangeData = (projected, lower, upper) => {
    let range = []
    let prevLower = 0
    let prevUpper = 0
    const currentMonth = (new Date()).getMonth() + 1

    for (let key of Object.keys(lower)) {
      let newUpper = 0
      let newLower = 0

      // The range should be computed so as to grow starting from "Today", not Jan.
      if (key < currentMonth) {
        newUpper = prevUpper + projected[key]
        newLower = prevLower + projected[key]
      } else {
        newUpper = prevUpper + upper[key]
        newLower = prevLower + lower[key]
      }
      const x = parseInt(key)  //x values are calculated from 0, whereas keys start from 1, so we need to handle it

      prevLower = newLower
      prevUpper = newUpper
      range.push([x, newLower, newUpper])

    }
    return range
  }

  const getPrevxCategoriesElem = (val) => {
    const nameIndex = xCategories.indexOf(val)
    if (nameIndex === -1 || nameIndex-1 < 0)
      return 'ERROR'
    return xCategories[nameIndex - 1]
  }

  const getMonthIndex = (month) =>{
    return xCategories.indexOf(month)
  }

  const currentDayPosition = () => {
    let currentDate = new Date()

    const months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    const currentYear = currentDate.getFullYear()
    const currentMonth = currentDate.getMonth()
    const currentDay = currentDate.getDate()

    let maxDayInMonth = months[currentMonth]

    if (currentYear % 4 === 0 && currentMonth === 1) {
      maxDayInMonth = 29
    }

    return currentMonth + currentDay / maxDayInMonth
  }

  const options = {
    title: null,
    credits: {
      enabled: false,
    },
    legend: {
      layout: "horizontal",
      align: "center",
      verticalAlign: "top",
      margin: 30
    },
    yAxis: {
      title: null,
      min: 0,
      floor: 0,
      endOnTick: true,
      startOnTick: true,
      lineWidth: 1,
      lineColor: "black",
    },
    xAxis: {
      categories: xCategories,
      type: 'category',
      title: null,
      labels: {
        step: 1,
        staggerLines: 2,
      },
      lineColor: "black",
      gridLineWidth: 1,
      showLastLabel: true,
      startOnTick: true,
      endOnTick: true,
      tickmarkPlacement: 'on',
      plotLines: [{
        label: {
          text: "Today",
          align: "center",
          verticalAlign: "center",
          textAlign: "center",
          y: -10,
          style: {
            color: '#767373',
          },
          rotation: 0
        },
        color: '#767373',
        width: 1,
        dashStyle: 'Dash',
        value: currentDayPosition()
      }]
    },
    series: [
      {
        name: "Last Year",
        type: "line",
        data: toSumArray(!!data && data["LAST_YEAR"]),
        color: "#4c7cda",
        marker: {
          symbol: "circle"
        }
      },
      {
        name: "YTD",
        type: "line",
        data: toSumArray(!!data && data["CURRENT_YEAR"]),
        color: "#067008",
        marker: {
          symbol: "circle"
        }
      },
      {
        name: "Projected",
        type: "line",
        data: toSumArray(!!data && data["PROJECTED"]),
        color: "#f1855e",
        marker: {
          symbol: "circle"
        },
        dashStyle: 'dot',
        zoneAxis: 'x',
        // hiding displaying data before currentDayPosition
        zones: [
          {
            value: currentDayPosition(),
            color: 'transparent',
          }
        ]
      },
      {
        name: 'StDevRange',
        data: rangeData(!!data && data["PROJECTED"], !!data && data["PROJECTED_STDEV_LOWER"], !!data && data["PROJECTED_STDEV_UPPER"]),
        type: 'arearange',
        lineWidth: 0,
        fillOpacity: 0.5,
        showInLegend: false,
        zoneAxis: 'x',
        color: '#f3ccbe',
        // hiding displaying data before currentDayPosition
        zones: [
          {
            value: currentDayPosition(),
            color: 'none'
          }
        ]
      }
    ],
    tooltip: {
      shared: true,
      valuePrefix: '$',
      distance: 40,
      useHTML: true,
      backgroundColor: "white",
      formatter: function () {
        let styles = this.points.filter(({point}) => point.color !== 'none').reduce(function (s, point) {
          // Do not display the tooltip for the first point
          if (point.x === xCategories[0])
            return false
          // here we are handling the Range series and formatting tooltip for these lines
          if (point.point.low && point.point.high) {
            return `${s}<div style="margin-top: 5px"><span style="color:${point.color}">● </span> Projected + 1 year stdev: ${formatMoney(point.point.high)}</div>
                        <div style="margin-top: 5px"><span style="color:${point.color}">● </span> Projected - 1 year stdev: ${formatMoney(point.point.low)}</div>`;
          }
          if (getMonthIndex(point.x) < currentDayPosition() && point.series.name === 'Projected'){
            return s
          }
          return `${s}<div style="margin-top: 5px"><span style="color:${point.color}">● </span> ${point.series.name}: ${formatMoney(point.y)}</div>`;
        }, `<div style="font-weight: bold"> ${getPrevxCategoriesElem(this.x)} ● Gross Income </div>`);

        if (!styles) return false
        return `<div style="display: flex; flex-direction: column">${styles}</div>`
      },
    },
    plotOptions: {
      series: {
        pointPlacement: 'on',
      }
    },
  };

  // Reset drawPoints function- it allows us to display bullets only on hover, not display bullets all the time
  Highcharts.Series.prototype.drawPoints = function () {
  };

  return <HighchartsReact highcharts={Highcharts} options={options}
                          constructorType={'chart'}/>;
};
