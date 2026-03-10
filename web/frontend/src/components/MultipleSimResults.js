import React from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';
import './MultipleSimResults.css';

const PROTOCOL_COLORS = {
  BB84:  '#4f7be8',
  B92:   '#f5a623',
  E91:   '#27ae60',
  BBM92: '#e74c3c',
};

const PROTOCOLS = ['BB84', 'B92', 'E91', 'BBM92'];

function formatY(value) {
  if (value === null || value === undefined || isNaN(value)) return '-';
  if (Math.abs(value) >= 1e6) return (value / 1e6).toFixed(2) + 'M';
  if (Math.abs(value) >= 1e3) return (value / 1e3).toFixed(1) + 'k';
  return parseFloat(value.toFixed(4)).toString();
}

function MultipleSimResults({ results, xLabel, yLabel }) {
  // results: { x_values: [...], data: { BB84: [...], B92: [...], E91: [...], BBM92: [...] } }
  return (
    <div className="multi-results-container">
      <h2>Simulation Results</h2>
      <p className="multi-results-subtitle">
        <strong>{yLabel}</strong> vs <strong>{xLabel}</strong> — all 4 QKD protocols
      </p>

      <div className="multi-charts-grid">
        {PROTOCOLS.map(protocol => {
          const yVals = results.data[protocol] || [];
          const chartData = results.x_values.map((x, i) => ({
            x: parseFloat(x.toFixed(6)),
            y: yVals[i] !== undefined ? yVals[i] : null,
          }));

          return (
            <div key={protocol} className="chart-card">
              <div
                className="chart-card-header"
                style={{ borderLeftColor: PROTOCOL_COLORS[protocol] }}
              >
                <h3 style={{ color: PROTOCOL_COLORS[protocol] }}>{protocol}</h3>
              </div>

              <ResponsiveContainer width="100%" height={260}>
                <LineChart
                  data={chartData}
                  margin={{ top: 10, right: 20, left: 10, bottom: 40 }}
                >
                  <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
                  <XAxis
                    dataKey="x"
                    label={{ value: xLabel, position: 'insideBottom', offset: -20, fontSize: 12 }}
                    tick={{ fontSize: 11 }}
                    tickFormatter={(v) => parseFloat(v.toFixed(4))}
                  />
                  <YAxis
                    tick={{ fontSize: 11 }}
                    width={72}
                    tickFormatter={formatY}
                    label={{ value: yLabel, angle: -90, position: 'insideLeft', offset: 10, fontSize: 12 }}
                  />
                  <Tooltip
                    formatter={(value) => [
                      value !== null ? formatY(value) : '-',
                      yLabel,
                    ]}
                    labelFormatter={(label) => `${xLabel}: ${parseFloat(label.toFixed ? label.toFixed(4) : label)}`}
                  />
                  <Line
                    type="monotone"
                    dataKey="y"
                    stroke={PROTOCOL_COLORS[protocol]}
                    strokeWidth={2}
                    dot={{ r: 4, fill: PROTOCOL_COLORS[protocol] }}
                    activeDot={{ r: 6 }}
                    connectNulls={false}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default MultipleSimResults;
