using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.Extensions.Logging;

namespace Tracker.Pages
{
    public class Login : PageModel
    {
        private readonly ILogger<Login> _logger;

        public Login(ILogger<Login> logger)
        {
            _logger = logger;
        }

        public void OnGet()
        {
        }
    }
}