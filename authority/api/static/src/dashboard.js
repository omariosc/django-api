// dashboard.js

function groupBy(data, key) {
  return data.reduce((acc, item) => {
    (acc[item[key]] = acc[item[key]] || []).push(item);
    return acc;
  }, {});
}

function sum(arr, key) {
  return arr.reduce((acc, item) => acc + item[key], 0);
}

async function fetchAndRenderPassengersPerAirlineTodayChart() {
  const response = await fetch("/passengers-per-airline-today/");
  const data = await response.json();
  renderBarChart(
    "passengers-per-airline-today",
    data,
    "airline_name",
    "passengers"
  );
}

async function fetchAndRenderIncomePerFlightCharts() {
  const [flightsResponse, airportsResponse] = await Promise.all([
    fetch("/income-per-flight/"),
    fetch("/api/airports/"),
  ]);

  const flightsData = await flightsResponse.json();
  const airportsData = await airportsResponse.json();

  const airportsById = {};
  airportsData.forEach((airport) => (airportsById[airport.id] = airport));

  const groupedByAirline = groupBy(flightsData, "airline");
  const groupedByAirport = groupBy(flightsData, "origin_airport");
  const groupedByCity = groupBy(
    flightsData,
    (flight) => airportsById[flight.origin_airport].city
  );
  const groupedByCountry = groupBy(
    flightsData,
    (flight) => airportsById[flight.origin_airport].country
  );

  renderBarChart(
    "income-per-airline",
    groupedByAirline,
    "airline_name",
    "income"
  );
  renderBarChart(
    "income-per-airport",
    groupedByAirport,
    "origin_airport",
    "income"
  );
  renderBarChart("income-per-city", groupedByCity, "origin_city", "income");
  renderBarChart(
    "income-per-country",
    groupedByCountry,
    "origin_country",
    "income"
  );
}

function renderBarChart(elementId, groupedData, labelKey, valueKey) {
  const ctx = document.getElementById(elementId).getContext("2d");
  const labels = Object.keys(groupedData);
  const values = labels.map((label) => sum(groupedData[label], valueKey));

  const chart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Income",
          data: values,
          backgroundColor: "rgba(75, 192, 192, 0.2)",
          borderColor: "rgba(75, 192, 192, 1)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
}

// Fetch data and render charts
fetchAndRenderPassengersPerAirlineTodayChart();
fetchAndRenderIncomePerFlightCharts();
