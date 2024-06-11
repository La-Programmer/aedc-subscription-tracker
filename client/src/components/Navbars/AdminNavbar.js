import React, { useState, useEffect } from 'react';
import { Navbar, Container, Nav, Dropdown, Button } from 'react-bootstrap';

function Header() {
  const [navbarWidth, setNavbarWidth] = useState('100%');

  useEffect(() => {
    const handleResize = () => {
      setNavbarWidth(window.innerWidth > 600 ? '82%' : '100%');
    };

    // Set initial width
    handleResize();

    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  const navbarStyle = {
    position: 'fixed',
    zIndex: '1',
    width: navbarWidth,
    top: 0,
  };

  const mainContentStyle = {
    marginTop: '110px', // Adjust this value based on your actual Navbar height
  };

  return (
    <div>
      <Navbar bg="light" expand="lg" style={navbarStyle}>
        <Container fluid>
          <div className="d-flex justify-content-center align-items-center ml-2 ml-lg-0">
            <Button
              variant="dark"
              className="d-lg-none btn-fill d-flex justify-content-center align-items-center rounded-circle p-2"
              onClick={e => {
                e.preventDefault();
                document.documentElement.classList.toggle('nav-open');
                const node = document.createElement('div');
                node.id = 'bodyClick';
                node.onclick = function () {
                  this.parentElement.removeChild(this);
                  document.documentElement.classList.toggle('nav-open');
                };
                document.body.appendChild(node);
              }}
            >
              <i className="fas fa-ellipsis-v"></i>
            </Button>
            <Navbar.Brand
              href="#home"
              onClick={e => e.preventDefault()}
              className="mr-2"
            >
              <div style={{ display: 'flex', alignItems: 'center' }}>
                <img
                  className="d-none d-lg-block"
                  style={{ width: '100px', height: '40px', marginLeft: '-20px' }}
                  src={require('assets/img/aedc-logo.png')}
                  alt="..."
                />
                <span
                  style={{
                    fontFamily: 'Roboto, sans-serif',
                    color: '#012970',
                  }}
                  className="no-icon"
                >
                  Subscription Management System
                </span>
              </div>
            </Navbar.Brand>
          </div>
          <Navbar.Toggle aria-controls="basic-navbar-nav" className="mr-2">
            <span className="navbar-toggler-bar burger-lines"></span>
            <span className="navbar-toggler-bar burger-lines"></span>
            <span className="navbar-toggler-bar burger-lines"></span>
          </Navbar.Toggle>
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="nav mr-auto" navbar></Nav>
            <Nav className="ml-auto" navbar>
              <Dropdown as={Nav.Item}>
                <Dropdown.Toggle
                  aria-expanded={false}
                  aria-haspopup={true}
                  as={Nav.Link}
                  data-toggle="dropdown"
                  id="navbarDropdownMenuLink"
                  variant="default"
                  className="m-0"
                >
                  <span style={{ color: '#012970' }} className="no-icon">
                    Isaac.Medugu@abujaelectricity.com
                  </span>
                </Dropdown.Toggle>
                <Dropdown.Menu aria-labelledby="navbarDropdownMenuLink">
                  <Dropdown.Item href="#pablo" onClick={e => e.preventDefault()}>
                    Action
                  </Dropdown.Item>
                  <Dropdown.Item href="#pablo" onClick={e => e.preventDefault()}>
                    Another action
                  </Dropdown.Item>
                  <Dropdown.Item href="#pablo" onClick={e => e.preventDefault()}>
                    Something
                  </Dropdown.Item>
                  <Dropdown.Item href="#pablo" onClick={e => e.preventDefault()}>
                    Something else here
                  </Dropdown.Item>
                  <div className="divider"></div>
                  <Dropdown.Item href="#pablo" onClick={e => e.preventDefault()}>
                    Separated link
                  </Dropdown.Item>
                </Dropdown.Menu>
              </Dropdown>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
      <div style={mainContentStyle}>
        {/* Your main content here */}
      </div>
    </div>
  );
}

export default Header;
