// function to add Event listeners for Skill value form field validation
function addSkillValueValidationEvent(fieldId) {
    let skillValueField = document.getElementById(`id_skill-${fieldId}-value`);
    let skillDeleteFlag = document.getElementById(`id_skill-${fieldId}-DELETE`);
    skillValueField.oninput = () => {
        skillValuesValidation();
    }
    skillDeleteFlag.oninput = () => {
        skillValuesValidation();
    }
}

// function used during window.onload to initialize Event listeners on Skill value form fields for validation
function eventListenerInit() {
    // get TOTAL_FORMS element from Django management_form of Skill formset
    let totalSkillForms = document.getElementById("id_skill-TOTAL_FORMS");
    for (i = 0; i < totalSkillForms.value; i++) {
        addSkillValueValidationEvent(i);
    }
}

// function to dynamically add new skill fieldsets on Character forms
function addSkill() {
            // get TOTAL_FORMS element from Django management_form of Skill formset
            let totalSkillForms = document.getElementById("id_skill-TOTAL_FORMS");
            // get MAX_NUM_FORMS element from Django management_form of Skill formset
            let maxSkillForms = document.getElementById("id_skill-MAX_NUM_FORMS");
            // only add new Skill fieldset if MAX_NUM_FORMS not reached yet
            if (totalSkillForms.value !== maxSkillForms.value) {
                // get all Skill fieldsets
                const skillFieldSets = document.getElementsByClassName("skill");
                // get last Skill fieldset
                const lastSkill = skillFieldSets[skillFieldSets.length - 1];
                // clone last Skill fieldset
                let clone = lastSkill.cloneNode(true);
                // replace upcounting number in clone inner HTML
                const count = String(parseInt(totalSkillForms.value) - 1);
                const regex = new RegExp(count, "g");
                clone.innerHTML = clone.innerHTML.replace(regex, totalSkillForms.value);
                // get DIV of Skill fieldsets
                let skills = document.getElementById("skills");
                // append clone to DIV
                skills.appendChild(clone);
                // add Skill Value Validation Event to newly created Skill Value field
                addSkillValueValidationEvent(totalSkillForms.value);
                // increase TOTAL_FORMS element to comply with Django logic
                totalSkillForms.value = String(parseInt(totalSkillForms.value) + 1);
            } else {
                // deactivate add Skill button in case MAX_NUM_FORMS reached
                button = document.getElementById("addSkill");
                button.setAttribute("disabled", true);
            }
        }

// function to validate overall Skill values - should not exceed 400
function skillValuesValidation() {
    // get TOTAL_FORMS element from Django management_form of Skill formset
    let totalSkillForms = document.getElementById("id_skill-TOTAL_FORMS");
    let skillValues = [];
    // iterate Skill value fields and collect valid values
    for (i = 0; i < totalSkillForms.value; i++) {
        let skillDeleteFlag = document.getElementById(`id_skill-${i}-DELETE`).checked;
        let skillValue = document.getElementById(`id_skill-${i}-value`).value;
        if (!skillDeleteFlag && skillValue !== "") {
            skillValues.push(parseInt(skillValue));
        }
    }
    // sum up Skill values
    const valuesSum = skillValues.reduce((a, b) => a + b, 0);
    // calculate remaining Skill Points
    const remainingPoints = 400 - valuesSum;
    let skillPointsRemaining = document.getElementById("skill-points-remaining");
    // adapt Frontend message
    skillPointsRemaining.innerHTML = `Remaining Skill Points: ${remainingPoints}`;
    // handle Submit Button state
    if (remainingPoints !== 0) {
        document.getElementById("characterSubmit").disabled = true;
    } else {
        document.getElementById("characterSubmit").disabled = false;
    }
}