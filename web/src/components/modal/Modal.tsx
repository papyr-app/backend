import React, { useEffect } from 'react';
import './Modal.scss';

interface ModalProps {
    show: boolean;
    onClose?: () => void;
    children?: React.ReactNode;
}

export default function Modal(props: ModalProps) {
    useEffect(() => {
        const handleKeyDown = (event: KeyboardEvent) => {
            if (event.key === 'Escape' && props.onClose) {
                props.onClose();
            }
        };

        if (props.show) {
            document.addEventListener('keydown', handleKeyDown);
        } else {
            document.removeEventListener('keydown', handleKeyDown);
        }

        return () => {
            document.removeEventListener('keydown', handleKeyDown);
        };
    }, [props.show, props.onClose]);

    if (!props.show) {
        return null;
    }

    return (
        <div className="modal-overlay">
            <div className="modal">
                {props.children}
                <button className='button-primary' onClick={props.onClose}>Close</button>
            </div>
        </div>
    );
}
