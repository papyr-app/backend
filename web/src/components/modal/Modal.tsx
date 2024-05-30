import React  from 'react';
import './Modal.scss';

interface ModalProps {
    show: boolean;
    onClose?: () => void;
    children?: React.ReactNode;
}

export default function Modal(props: ModalProps) {
    if (!props.show) {
        return null;
    }

    return (
        <div className="modal-overlay">
            <div className="modal">
                <button className='button-primary' onClick={props.onClose}>Close</button>
                {props.children}
            </div>
        </div>
    );
}
