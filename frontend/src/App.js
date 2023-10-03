import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';

const socket = io('http://localhost:5001'); // Replace with the actual server URL

function App() {
  const [sensorData, setSensorData] = useState([]);
  
  useEffect(() => {
    socket.on('sensor_data', (data) => {
      setSensorData((prevData) => [...prevData, data]);
    });

    return () => {
      socket.off('sensor_data');
    };
  }, []);

  // Function to clear the sensor data
  const handleClearData = () => {
    setSensorData([]);
  };

  return (
    <div className="App">
      <h1>Shopping Cart:</h1>
      <button onClick={handleClearData}>Clear Data</button>
      <table>
        <thead>
          <tr>
            <th>Items</th>
            <th>Weight (lbs)</th>
            <th>Cost ($)</th>
          </tr>
        </thead>
        <tbody>
          {sensorData.map((data, index) => (
            <tr key={index}>
              <td>{data.item}</td>
              <td>{data.weight}</td>
              <td>{data.cost}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
