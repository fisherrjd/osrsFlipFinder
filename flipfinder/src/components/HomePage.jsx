import React, {Component} from 'react';
import axios from 'axios';
import {Link} from 'react-router-dom';

class HomePage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      items: [],
      baseMargin: 0,
      filteredItems: [],
      sortState: null
    };
  }

  componentDidMount() {
    axios.get(`http://${window.location.host}/api/margin`).then((response) => {
      this.setState({items: response.data.items});
    });
  }

  handleInputChange = (event) => {
    const { name, value } = event.target;
    this.setState({ [name]: value }, () => {
      const { items, baseMargin } = this.state;
      const filteredItems = items.filter(
        (item) => Number(item.Margin.replace(/[^0-9.-]+/g,"")) >= Number(baseMargin)
      );
      this.setState({ filteredItems });
    });
  };

  handleSort = (column) => {
    const { sortState, filteredItems } = this.state;
    let newSortState;
  
    if (sortState === column) {
      newSortState = column === "Name" ? "NameDesc" : "MarginDesc";
    } else {
      newSortState = column === "Name" ? "NameAsc" : "MarginAsc";
    }
  
    const sortedItems = filteredItems.slice().sort((a, b) => {
      if (column === "Name" || column === "NameAsc" || column === "NameDesc") {
        return a.Name.localeCompare(b.Name);
      } else {
        return a.Margin - b.Margin;
      }
    });
  
    if (newSortState.endsWith("Desc")) {
      sortedItems.reverse();
    }
  
    this.setState({ sortState: newSortState, filteredItems: sortedItems });
  };

  render() {
    const {items, baseMargin, filteredItems} = this.state;
    const dataToRender = baseMargin > 0 ? filteredItems : items;
    return (
      <>
        <label htmlFor="baseMargin">Enter base margin:</label>
        <input
          type="number"
          name="baseMargin"
          value={baseMargin}
          onChange={this.handleInputChange}
        />
        <table>
          <tbody>
            <tr>
              <th>Name</th>
              <th onClick={() => this.handleSort("Margin")}>Margin</th>
            </tr>
            {dataToRender.map((item) => (
              <tr key={item.id}>
                <td>
                  <Link to={`/itemdetails/${item.id}`}>{item.Name}</Link>
                </td>
                <td>{item.Margin}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </>
    );
  }
}

export default HomePage;
