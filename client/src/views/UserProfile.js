import React, { useState, } from "react";
import { Button, Card, Form, Container, Row, Col } from "react-bootstrap";

function User() {
  // State to store form data
  const [formData, setFormData] = useState({
    subscriptionName: "",
    emails: "", // Single input for multiple emails
    startDate: "",
    expiryDate: "",
    description: ""
  });

  // State to manage loading state
  const [loading, setLoading] = useState(false);

  // State to manage submission status
  const [submissionStatus, setSubmissionStatus] = useState(null);

  // Function to handle form submission
  const handleSubmit = (event) => {
    event.preventDefault();
    setLoading(true); // Set loading state to true while form is being submitted
    const url = 'https://dummy.restapiexample.com/api/v1/create'; // URL to post form data

    // Process emails input into an array
    const emailsArray = formData.emails.split(',').map(email => email.trim());

    // Create payload including emails array
    const payload = {
      ...formData,
      emails: emailsArray
    };

    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    })
      .then(response => {
        console.log(response);
        console.log(payload);
        if (response.ok) {
          setSubmissionStatus("success");
          setFormData({
            subscriptionName: "",
            emails: "",
            startDate: "",
            expiryDate: "",
            description: ""
          });
        } else {
          setSubmissionStatus("error");
        }
      })
      .catch(error => {
        console.error("Error:", error);
        setSubmissionStatus("error");
      })
      .finally(() => {
        setLoading(false); // Set loading state back to false after form submission
      });
  };

  // Function to handle form input changes
  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  return (
    <>
      {loading && <div className="loading">Submitting...</div>}
      {submissionStatus && (
        <div className={`submission-status ${submissionStatus}`}>
          {submissionStatus === "success" ? "Form submitted successfully" : "Failed to submit form"}
        </div>
      )}
      <Container fluid>
        <Row className="justify-content-center">
          <Col md="12">
            <Card style={{ width: "100%", height: "100%" }}>
              <Card.Header style={{ backgroundColor: "#012970", color: "white", fontFamily: "Roboto, sans-serif", padding: "15px 20px" }}>
                <Card.Title as="h4" style={{ color: "white", margin: "0" }}>Subscription Form</Card.Title>
              </Card.Header>
              <Card.Body>
                <Form onSubmit={handleSubmit}>
                  <Row>
                    <Col md="6">
                      <Form.Group>
                        <label style={{ fontFamily: "Roboto, sans-serif" }}>Subscription Name</label>
                        <Form.Control
                          placeholder="Subscription"
                          type="text"
                          name="subscriptionName"
                          value={formData.subscriptionName}
                          onChange={handleInputChange}
                          style={{ fontFamily: "Roboto, sans-serif" }}
                        ></Form.Control>
                      </Form.Group>
                    </Col>
                    <Col md="6">
                      <Form.Group>
                        <label htmlFor="exampleInputEmail1" style={{ fontFamily: "Roboto, sans-serif" }}>
                          Stakeholder Email Addresses (comma-separated)
                        </label>
                        <Form.Control
                          placeholder="Emails"
                          type="text"
                          name="emails"
                          value={formData.emails}
                          onChange={handleInputChange}
                          style={{ fontFamily: "Roboto, sans-serif" }}
                        ></Form.Control>
                      </Form.Group>
                    </Col>
                  </Row>
                  <Row>
                    <Col md="6">
                      <Form.Group>
                        <label style={{ fontFamily: "Roboto, sans-serif" }}>Start Date</label>
                        <Form.Control
                          type="datetime-local"
                          id="start-date"
                          name="startDate"
                          value={formData.startDate}
                          onChange={handleInputChange}
                          style={{ fontFamily: "Roboto, sans-serif" }}
                        ></Form.Control>
                      </Form.Group>
                    </Col>
                    <Col md="6">
                      <Form.Group>
                        <label style={{ fontFamily: "Roboto, sans-serif" }}>Expiry Date</label>
                        <Form.Control
                          type="datetime-local"
                          id="expiry-date"
                          name="expiryDate"
                          value={formData.expiryDate}
                          onChange={handleInputChange}
                          style={{ fontFamily: "Roboto, sans-serif" }}
                        ></Form.Control>
                      </Form.Group>
                    </Col>
                  </Row>
                  <Row>
                    <Col md="12">
                      <Form.Group>
                        <label style={{ fontFamily: "Roboto, sans-serif" }}>Subscription Description</label>
                        <Form.Control
                          cols="80"
                          placeholder="Here can be your description"
                          rows="4"
                          as="textarea"
                          name="description"
                          value={formData.description}
                          onChange={handleInputChange}
                          style={{ fontFamily: "Roboto, sans-serif" }}
                        ></Form.Control>
                      </Form.Group>
                    </Col>
                  </Row>
                  <Button
                    className="btn-fill pull-right"
                    type="submit"
                    variant="info"
                    style={{ backgroundColor: "#012970", border: "none", fontFamily: "Roboto, sans-serif" }}
                  >
                    {loading ? "Submitting..." : "Submit"}
                  </Button>
                  <div className="clearfix"></div>
                </Form>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </>
  );
}

export default User;
