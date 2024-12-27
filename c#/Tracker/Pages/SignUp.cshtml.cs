using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.Extensions.Logging;

namespace Tracker.Pages
{
    public class SignUp : PageModel
    {
        private readonly ILogger<SignUp> _logger;

        public SignUp(ILogger<SignUp> logger)
        {
            _logger = logger;
        }

        public void OnGet()
        {
        }
    }
}