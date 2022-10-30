import React, { Component } from 'react'
import axios from "axios";



class GetItem extends Component{
  state = {
    items_details: []
  }
  constructor(){
    super();
    axios.get(`http://${window.location.host}/api/item/4151`).then(response => {
      this.setState({items_details: response.data})
      console.log(items_details)
    })
  }
  render(){
    return(
        <div>
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
              {this.state.items_details.map(item => (
                <tr key="item.id">
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

export default GetItem