import React, {Component} from 'react';
import axios from 'axios';
import {Link} from 'react-router-dom';
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
      <table className="rwd-table">
        <tbody>
          <tr>
            <th>Name</th>
            <th>Margin</th>
          </tr>
          {items.map((item) => (
            <tr key={item.id}>
              <td>
                <Link to={`/itemdetails/${item.id}`}>{item.name}</Link>
              </td>
              <td>{item.margin}</td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  }
}

export default PlaceholderHome;
