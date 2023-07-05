import * as React from "react";
import { SearchArticleTitle, GetRandomArticleTitles } from "@home/request";
import { Input, ListGroup, ListGroupItem } from "reactstrap";

interface IProps {
    onInputChange: (value: string) => void;
    disabled: boolean
}

function SearchInput(props: IProps) {
    const defaultVal: string[] = [] // So typescript doesnt cast to any[] xd
    const [inputResults, setInputResults] = React.useState(defaultVal);
    const [inputPreviousResults, setInputPreviousResults] = React.useState(defaultVal);
    const [inputPlaceholderVal, setInputPlaceholderVal] = React.useState("");

    async function handleInputChange(event: React.ChangeEvent<HTMLInputElement>) {
        props.onInputChange(event.currentTarget.value);

        if (event.currentTarget.value == "") {
            setInputResults([]);
            return;
        }

        // TODO: catch error lol
        const searchResult = await SearchArticleTitle(event.currentTarget.value);
        setInputResults(searchResult);
    }

    function inputBlurEvent() {
        setInputResults([]);
        setInputPreviousResults(inputResults);
    }

    function inputFocusEvent() {
        setInputResults(inputPreviousResults);
    }

    React.useEffect(() => {
        const interval = setInterval(async () => {
            const articleTitles = await GetRandomArticleTitles();
            let newVal = articleTitles[Math.floor(Math.random() * articleTitles.length)];

            for (let i = 0; i < newVal.length; i++) {
                setInputPlaceholderVal(newVal.slice(0, i+1));
                await new Promise(r => setTimeout(r, Math.ceil(1000 / newVal.length)));
            }
            await new Promise(r => setTimeout(r, 1000));

            // If you ever wonder why i dont use inputPlaceholderVal, its cus its empty for some reason
            const initialLength = newVal.length;
            while (newVal.length > 0) {
                newVal = newVal.slice(0, newVal.length - 1)
                setInputPlaceholderVal(newVal.slice(0, newVal.length - 1));
                
                await new Promise(r => setTimeout(r, 1000 / initialLength));
            }
        }, 3500);

        return () => clearInterval(interval);
    }, []);

    if (props.disabled && inputResults.length > 0) {
        inputBlurEvent();
    }
    
    return <>
        <Input bsSize="lg" onChange={handleInputChange} onBlur={inputBlurEvent} onFocus={inputFocusEvent} 
        placeholder={inputPlaceholderVal} 
        className="shadow"
        disabled={props.disabled}/>
        <ListGroup hidden={props.disabled}>
            <div style={{position: "absolute"}}>
                {inputResults.map(s => <ListGroupItem key={s}>{s}</ListGroupItem>)}
            </div>
        </ListGroup>
    </>
}

export default SearchInput;