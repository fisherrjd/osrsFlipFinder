import React, {Component, useState, useEffect} from 'react';
import axios from 'axios';
class PlaceholderHome extends Component {
  constructor(props) {
    super(props);
    this.state = {items: []};
  }
  componentDidMount() {
    axios.get(`http://${window.location.host}/api/margin`).then((response) => {
      this.setState({items: response.data.items});
      console.log(this.state.items);
    });
  }
  render() {
    const {items} = this.state;
    return (
      <div>
        <table className="rwd-table">
          <tbody>
            <tr>
              <th>
                <button>Name</button>
              </th>
              <th>ID</th>
              <th>High Price</th>
              <th>Low price</th>
              <th>Margin</th>
              <th>High Time</th>
              <th>Low Time</th>
            </tr>
            {items.map((item) => (
              <tr key={item.id}>
                <td>{item.name}</td>
                <td>{item.id}</td>
                <td>{item.high_price}</td>
                <td>{item.low_price}</td>
                <td>{item.margin}</td>
                <td>{item.highTime}</td>
                <td>{item.lowTime}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }
}

export default PlaceholderHome;

// {
//   /* <Link to={`/itemdetails/${item.id}`}></Link> */
// }
