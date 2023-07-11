import * as React from "react";
import { Container, Row, Col} from "reactstrap";
import "./errordisplay_style.scss";

export enum ErrorType {
    NO_PATH,
    INVALID_ARTICLE,
    INTERNAL_ERROR
}

export interface ErrorProps {
    type?: ErrorType;
    additionalInfo?: string;
}

function ErrorDisplay(props: ErrorProps) {
    let displayText = "An error happened";
    switch (props.type) {
        case ErrorType.NO_PATH:
            displayText = "No paths exist between those 2 articles!"
            break;
        case ErrorType.INVALID_ARTICLE:
            displayText = `Article "${props.additionalInfo}" doesn't exist`
            break;
        case ErrorType.INTERNAL_ERROR:
            displayText = "An error happened while fetching the server :("
            break;
    }

    return <Row className="error-display-row g-0 error-display-container shadow">
            <Col/>
            <Col md="7">
            <h4>{displayText}</h4>
            </Col>
            <Col/>
    </Row>
}

export default ErrorDisplay