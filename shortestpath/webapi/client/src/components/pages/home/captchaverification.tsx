import { doBotVerif } from "@home/request";
import * as React from "react";
import { Modal, ModalHeader, ModalBody } from "reactstrap";

interface Props {
    isOpen: boolean;
    verifCallback: (success: boolean) => void;
    closedCallback: () => void;
}

function CaptchaVerification(props: Props) {
    const [isOpen, setIsOpen] = React.useState(props.isOpen);
    const toggle = () => setIsOpen(!isOpen);

    React.useEffect(() => {
       setTimeout(() => {
        if (document.getElementById("recaptcha-verif") === null) return;

        grecaptcha.render("recaptcha-verif", {
            sitekey: BUILDCONFIG.recaptchaSiteKey,
            callback: async (response) => {
                try {
                    const success = await doBotVerif(response);
                    props.verifCallback(success);
                } catch (err) {
                    props.verifCallback(false);
                }
            }
        });
       }, 500);
    }, []);

    return <Modal isOpen={isOpen} toggle={toggle} onClosed={props.closedCallback}>
        <ModalHeader toggle={toggle}>Are you a robot?</ModalHeader>
        <ModalBody style={{margin: "auto"}}>
            <div id="recaptcha-verif"></div>
        </ModalBody>
    </Modal>
}

export default CaptchaVerification;