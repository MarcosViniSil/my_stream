import React, { useState } from 'react';
import MenuResponsive from '../../layout/menuReponsive/MenuReponsive';
import SendCode from '../../components/sendCode/sendCode';
import EnterCode from '../../components/enterCode/enterCode'
import UpdatePassword from '../../components/updatePassword/updatePassword'
export default function RecoverPassword() {
  const [isMenuOpen, setIsMenuOpen] = useState(true);

  const [step, setStep] = useState(1); // 1: enviar código, 2: digitar código, 3: alterar senha
  const [email, setEmail] = useState('');
  const [code, setCode] = useState('');

  const nextStep = () => setStep((s) => s + 1);
  const prevStep = () => setStep((s) => s - 1);

  return (
    <>
      <MenuResponsive isOpen={isMenuOpen} setIsOpen={setIsMenuOpen} />

      <div className={`wrapSendVideo ${isMenuOpen ? "menu-open" : ""}`}>
        {step === 1 && (
          <SendCode
            email={email}
            setEmail={setEmail}
            onSuccess={nextStep}
          />
        )}
        {step === 2 && (
          <EnterCode
            email={email}
            code={code}
            setCode={setCode}
            onSuccess={nextStep}
            onBack={prevStep}
          />
        )}
        {step === 3 && (
          <UpdatePassword
            email={email}
            code={code}
            onBack={prevStep}
          />
        )}
      </div>
    </>
  );
}
