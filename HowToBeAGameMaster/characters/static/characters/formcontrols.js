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
                // increase TOTAL_FORMS element to comply with Django logic
                totalSkillForms.value = String(parseInt(totalSkillForms.value) + 1);
            } else {
                // deactivate add Skill button in case MAX_NUM_FORMS reached
                button = document.getElementById("addSkill");
                button.setAttribute("disabled", true);
            }
        }