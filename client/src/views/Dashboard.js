import React, { useState } from "react";
import { Card, Container, Row, Col } from "react-bootstrap";
import TableList from "./TableList";

function Dashboard() {
  const [subscriptionCounts, setSubscriptionCounts] = useState({ Active: 0, Inactive: 0, Expired: 0 });

  return (
    <>
      <Container fluid>
        <Row>
          <Col lg="3" sm="6">
            <Card className="card-stats">
              <Card.Body>
                <div>
                  <i className="fas fa-list-alt mr-3" style={{ fontSize: "20px", color: "#012970" }}></i>
                  <p style={{color:"#012970", fontFamily: "Poppins", fontWeight: "500"}} >All Subscriptions</p>      
                </div>
              </Card.Body>
              <Card.Footer>
                <hr></hr>
                <div className="stats">
                  <Card.Title as="h3" style={{color: "#012970", fontFamily: "Nunito", fontWeight: "700"}}>{Object.values(subscriptionCounts).reduce((acc, count) => acc + count, 0)}</Card.Title>
                </div>
              </Card.Footer>
            </Card>
          </Col>

          <Col lg="3" sm="6">
            <Card className="card-stats">
              <Card.Body>
                <div>
                  <i className="fas fa-clipboard-check mr-3" style={{ fontSize: "20px", color: "#012970" }}></i>    
                  <p style={{color:"#012970", fontFamily: "Poppins", fontWeight: "500"}} >Active Subscriptions</p>
                </div>
              </Card.Body>
              <Card.Footer>
                <hr></hr>
                <div className="stats">
                  <Card.Title as="h3" style={{color: "#012970", fontFamily: "Nunito", fontWeight: "700"}}>{subscriptionCounts.Active}</Card.Title>
                </div>
              </Card.Footer>
            </Card>
          </Col>

          <Col lg="3" sm="6">
            <Card className="card-stats">
              <Card.Body>
                <div>
                  <i className="fas fa-ban mr-3" style={{ fontSize: "20px", color: "#012970" }}></i>
                  <p style={{color:"#012970", fontFamily: "Poppins", fontWeight: "500"}} >Inactive Subscriptions</p>
                </div>
              </Card.Body>
              <Card.Footer>
                <hr></hr>
                <div className="stats">
                  <Card.Title as="h3" style={{color: "#012970", fontFamily: "Nunito", fontWeight: "700"}}>{subscriptionCounts.Inactive}</Card.Title>
                </div>
              </Card.Footer>
            </Card>
          </Col>

          <Col lg="3" sm="6">
            <Card className="card-stats">
              <Card.Body>
                <div>
                  <i className="fas fa-calendar-times mr-3" style={{ fontSize: "20px", color: "#012970" }}></i>
                  <p style={{color:"#012970", fontFamily: "Poppins", fontWeight: "500"}} >Expired Subscriptions</p>
                </div>
              </Card.Body>
              <Card.Footer>
                <hr></hr>
                <div className="stats">
                  <Card.Title as="h3" style={{color: "#012970", fontFamily: "Nunito", fontWeight: "700"}}>{subscriptionCounts.Expired}</Card.Title>
                </div>
              </Card.Footer>
            </Card>
          </Col>
        </Row>
       
        <TableList setSubscriptionCounts={setSubscriptionCounts} />
      </Container>
    </>
  );
}

export default Dashboard;
