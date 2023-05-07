import React, {Component} from 'react';
import axios from 'axios';
import {Link} from 'react-router-dom';
import './Item.css'

class GetItem extends Component {
  constructor(props) {
    super(props);
    this.state = {
      item_details: [],
    };
  }

  componentDidMount() {
    axios.get(`http://${window.location.host}/api/item/` + this.props.id.id).then((response) => {
      this.setState({item_details: response.data.item});
    });
  }

  render() {
    const {item_details} = this.state;
    return (
      <div>
          <Link to={`/`}>Home</Link>

        <table>
          <tbody>
            <tr>
              <th>Name</th>
              <th>ID</th>
              <th>High Price</th>
              <th>Low price</th>
              <th>Margin</th>
              <th>High Time</th>
              <th>Low Time</th>
            </tr>
            {item_details.map((item) => (
              <tr key={item.id}>
                <td>{item.Name}</td>
                <td>{item.id}</td>
                <td>{item.High_Price}</td>
                <td>{item.Low_Price}</td>
                <td>{item.Margin}</td>
                <td>{item.High_Time}</td>
                <td>{item.Low_Time}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }
}

export default GetItem;
