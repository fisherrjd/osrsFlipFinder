import React, { Component } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './index.css'

class HomePage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      items: [],
      baseMargin: 0,
      filteredItems: [],
      sortColumn: null,
      sortDirection: null,
      currentPage: 1,
      itemsPerPage: 20,
    };
  }

  componentDidMount() {
    axios
      .get(`http://${window.location.host}/api/margin`)
      .then((response) => {
        this.setState({ items: response.data.items });
      });
  }

  handleInputChange = (event) => {
    const { name, value } = event.target;
    this.setState({ [name]: value }, () => {
      const { items, baseMargin } = this.state;
      const filteredItems = items.filter(
        (item) =>
          Number(item.Margin.replace(/[^0-9.-]+/g, '')) >= Number(baseMargin)
      );
      this.setState({ filteredItems });
    });
  };

  handleSort = (column) => {
    const { sortColumn, sortDirection, items, filteredItems, baseMargin } = this.state;
    let newSortColumn = column;
    let newSortDirection = 'asc';
  
    if (sortColumn === column && sortDirection === 'asc') {
      newSortDirection = 'desc';
    } else if (sortColumn === column && sortDirection === 'desc') {
      newSortColumn = null;
      newSortDirection = null;
    }
  
    const dataToSort = baseMargin > 0 ? filteredItems : items;
  
    const sortedItems = dataToSort.slice().sort((a, b) => {
      if (column === 'Margin') {
        return (
          Number(a.Margin.replace(/[^0-9.-]+/g, '')) -
          Number(b.Margin.replace(/[^0-9.-]+/g, ''))
        );
      } else {
        return a.Name.localeCompare(b.Name);
      }
    });
  
    if (newSortDirection === 'desc') {
      sortedItems.reverse();
    }
  
    if (baseMargin > 0) {
      this.setState({
        sortColumn: newSortColumn,
        sortDirection: newSortDirection,
        filteredItems: sortedItems,
      });
    } else {
      this.setState({
        sortColumn: newSortColumn,
        sortDirection: newSortDirection,
        items: sortedItems,
      });
    }
  };
  

  handlePageClick = (event) => {
    this.setState({
      currentPage: Number(event.target.id),
    });
  };

  render() {
    const {
      items,
      baseMargin,
      filteredItems,
      sortColumn,
      sortDirection,
      currentPage,
      itemsPerPage,
    } = this.state;
    const dataToRender = baseMargin > 0 ? filteredItems : items;
  
    // Logic for displaying items
    const indexOfLastItem = currentPage * itemsPerPage;
    const indexOfFirstItem = indexOfLastItem - itemsPerPage;
    const currentItems = dataToRender.slice(indexOfFirstItem, indexOfLastItem);
  
    // Logic for displaying page numbers
    const pageNumbers = [];
    for (let i = 1; i <= Math.ceil(dataToRender.length / itemsPerPage); i++) {
      pageNumbers.push(i);
    }
  
    return (
      
      <div className="homepage">
            <div className="input-container">
                <label htmlFor="baseMargin">Enter base margin:</label>
                <input
                type="number"
                name="baseMargin"
                value={baseMargin}
                onChange={this.handleInputChange}
                />
            </div>
            <div className="table-container">
                <table>
                <tbody>
                    <tr>
                    <th>Name</th>
                    <th
                        onClick={() => this.handleSort('Margin')}
                        style={{ cursor: 'pointer' }}
                    >
                        Margin
                        {sortColumn === 'Margin' && sortDirection === 'asc' && (
                        <span>&#9650;</span>
                        )}
                        {sortColumn === 'Margin' && sortDirection === 'desc' && (
                        <span>&#9660;</span>
                        )}
                    </th>
                    </tr>
                    {currentItems.map((item) => (
                    <tr key={item.Id}>
                        <td>
                        <Link to={`/item/${item.id}`}
                        onClick={() => console.log(`Item ID: ${item.id}`)}
                        >{item.Name}</Link>
                        </td>
                        <td>{item.Margin}</td>
                    </tr>
                    ))}
                </tbody>
                </table>
            
                <div class ="pagification" style={{display: 'flex', justifyContent: 'center' }}>
                {pageNumbers.map((number) => (
                    <div class = "pageNumber"
                    key={number}
                    id={number}
                    onClick={this.handlePageClick}

                    >
                    {number}
                    </div>
                ))}
                </div>
                
            </div>
        </div>
      
    );
  }}

  export default HomePage;